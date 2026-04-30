import chromadb
import requests
import os
import re
import math
import sys
from pathlib import Path
from collections import Counter
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, SUGGEST_QUESTIONS_SYSTEM_PROMPT, SUGGEST_QUESTIONS_USER_PROMPT

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
EMBEDDING_URL = os.getenv("EMBEDDING_URL", "http://localhost:11434/api/embeddings")
GENERATION_MODEL = os.getenv("GENERATION_MODEL", "llama3.2")
GENERATION_URL = os.getenv("GENERATION_URL", "http://localhost:11434/api/generate")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "finance_docs")

RRF_K = 60
TOP_K = 5

STOPWORDS = {
    "the", "and", "or", "a", "an", "in", "on", "at", "to", "for",
    "of", "with", "is", "it", "this", "that", "are", "was", "be",
    "as", "by", "from", "but", "not", "have", "has", "had",
}


def get_chroma_client():
    try:
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        client.heartbeat()
        return client
    except Exception:
        return chromadb.PersistentClient(path="./data/chroma")


def get_collection():
    return get_chroma_client().get_collection(COLLECTION_NAME)


def embed_text(text: str) -> list[float]:
    resp = requests.post(
        EMBEDDING_URL,
        json={"model": EMBEDDING_MODEL, "prompt": text},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]


def generate_answer(system_prompt: str, user_prompt: str) -> str:
    resp = requests.post(
        GENERATION_URL,
        json={
            "model": GENERATION_MODEL,
            "prompt": f"{system_prompt}\n\n{user_prompt}",
            "stream": False,
        },
        timeout=180,
    )
    resp.raise_for_status()
    return resp.json()["response"].strip()


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z]+", text.lower())


class BM25:
    def __init__(self, corpus: list[dict], k1: float = 1.5, b: float = 0.75):
        self.corpus = corpus
        self.doc_tokens = [_tokenize(doc["text"]) for doc in corpus]
        self.term_freqs = [Counter(tokens) for tokens in self.doc_tokens]
        self.doc_lengths = [len(t) for t in self.doc_tokens]
        self.avg_dl = sum(self.doc_lengths) / max(1, len(self.doc_lengths))
        df = Counter()
        for tokens in self.doc_tokens:
            for term in set(tokens):
                df[term] += 1
        n = len(self.doc_tokens)
        self.idf = {
            term: math.log(1 + (n - freq + 0.5) / (freq + 0.5))
            for term, freq in df.items()
        }
        self.k1 = k1
        self.b = b

    def search(self, query: str, top_k: int = 10) -> list[tuple[float, dict]]:
        q_tokens = [t for t in _tokenize(query) if t not in STOPWORDS]
        if not q_tokens:
            return []
        scores = []
        for idx, tf in enumerate(self.term_freqs):
            dl = self.doc_lengths[idx]
            score = 0.0
            for term in q_tokens:
                if term not in tf:
                    continue
                idf = self.idf.get(term, 0.0)
                freq = tf[term]
                denom = freq + self.k1 * (1 - self.b + self.b * dl / max(1.0, self.avg_dl))
                score += idf * freq * (self.k1 + 1) / denom
            if score > 0:
                scores.append((score, self.corpus[idx]))
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:top_k]


def build_index(collection) -> BM25:
    all_data = collection.get(include=["documents", "metadatas"])
    corpus = [
        {"id": id_, "text": doc, "meta": meta}
        for id_, doc, meta in zip(
            all_data["ids"], all_data["documents"], all_data["metadatas"]
        )
    ]
    return BM25(corpus)


def rrf_combine(
    dense_results: list[dict],
    bm25_results: list[tuple[float, dict]],
    top_k: int = TOP_K,
) -> list[dict]:
    scores: dict[str, float] = {}
    docs: dict[str, dict] = {}

    for rank, result in enumerate(dense_results):
        key = result["id"]
        scores[key] = scores.get(key, 0.0) + 1 / (RRF_K + rank)
        docs[key] = result

    for rank, (_, result) in enumerate(bm25_results):
        key = result["id"]
        scores[key] = scores.get(key, 0.0) + 1 / (RRF_K + rank)
        docs[key] = result

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [docs[key] for key, _ in ranked[:top_k]]


def suggest_questions(survey_summary: str) -> list[str]:
    user_prompt = SUGGEST_QUESTIONS_USER_PROMPT.format(survey_summary=survey_summary)
    raw = generate_answer(SUGGEST_QUESTIONS_SYSTEM_PROMPT, user_prompt)
    questions = [line.strip() for line in raw.strip().splitlines() if line.strip()]
    return questions[:4]


def ask(question: str, collection, bm25: BM25) -> tuple[list[dict], str]:
    question_embedding = embed_text(question)

    dense_raw = collection.query(
        query_embeddings=[question_embedding],
        n_results=10,
        include=["documents", "metadatas", "distances"],
    )
    dense_results = [
        {"id": id_, "text": doc, "meta": meta}
        for id_, doc, meta in zip(
            dense_raw["ids"][0],
            dense_raw["documents"][0],
            dense_raw["metadatas"][0],
        )
    ]

    bm25_results = bm25.search(question, top_k=10)
    results = rrf_combine(dense_results, bm25_results)

    context = "\n\n".join(r["text"] for r in results)
    user_prompt = USER_PROMPT_TEMPLATE.format(question=question, context=context)
    answer = generate_answer(SYSTEM_PROMPT, user_prompt)
    return results, answer


def main() -> None:
    collection = get_collection()
    print("Building BM25 index...")
    bm25 = build_index(collection)

    question = input("What do you want to know?\n> ").strip()
    if not question:
        print("No question entered.")
        return

    print("Searching...")
    results, answer = ask(question, collection, bm25)

    print("\n--- Sources ---")
    for i, r in enumerate(results):
        print(f"{i + 1}. {r['meta'].get('source', '')} — {r['meta'].get('headings', '')}")

    print("\n--- Answer ---")
    print(answer)


if __name__ == "__main__":
    main()

from docling_core.types import DoclingDocument
from docling_core.transforms.chunker import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from pathlib import Path
import json
import requests
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
EMBEDDING_URL = os.getenv("EMBEDDING_URL", "http://localhost:11434/api/embeddings")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "finance_docs")

json_folder = Path("./data/processed/json")  # Run from project root


def get_chroma_client():
    try:
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        client.heartbeat()
        return client
    except Exception:
        print("Chroma server unreachable, falling back to local persistent client.")
        return chromadb.PersistentClient(path="./data/chroma")


def embed_text(text: str) -> list[float]:
    resp = requests.post(
        EMBEDDING_URL,
        json={"model": EMBEDDING_MODEL, "prompt": text},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]


# 512 tokens: mid-range of the team's 400-600 target, fits nomic-embed-text's
# 8192-token context comfortably while keeping chunks focused enough for precise retrieval.
# The tokenizer vocabulary (all-MiniLM-L6-v2) is used only for counting — actual
# embedding is done by Ollama separately.
tokenizer = HuggingFaceTokenizer.from_pretrained(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    max_tokens=512,
)
chunker = HybridChunker(tokenizer=tokenizer, merge_peers=True)

client = get_chroma_client()
collection = client.get_or_create_collection(
    COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)

for json_file in json_folder.glob("*.json"):
    print(f"Processing {json_file.stem}...")

    doc = DoclingDocument.model_validate_json(json_file.read_text(encoding="utf-8"))
    chunks = list(chunker.chunk(dl_doc=doc))

    # Save chunks to file for inspection/debugging
    with open(json_file.parent.parent / "chunks" / f"{json_file.stem}_chunks.json", "w", encoding="utf-8") as f:
        json_chunks = [chunk.model_dump() for chunk in chunks]
        f.write(json.dumps(json_chunks, indent=2))

    ids, embeddings, documents, metadatas = [], [], [], []

    for i, chunk in enumerate(chunks):
        # contextualize() prepends section headings to the chunk text before embedding
        # so the vector captures "where in the document" without duplicating headings
        # inside chunk.text itself
        text_to_embed = chunker.contextualize(chunk)
        embedding = embed_text(text_to_embed)

        ids.append(f"{json_file.stem}_{i}")
        embeddings.append(embedding)
        documents.append(chunk.text)
        metadatas.append({
            "source": json_file.stem,
            "headings": " > ".join(chunk.meta.headings or []),
        })

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )
    print(f"  {len(chunks)} chunks added from {json_file.stem}")

print("Done.")

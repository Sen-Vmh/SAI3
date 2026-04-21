SYSTEM_PROMPT = (
    "You are a helpful assistant. "
    "Answer questions only using the provided context. "
    "If the context does not contain enough information, say so."
)

USER_PROMPT_TEMPLATE = """Answer the following question using only the provided context.

Question: {question}

Context:
{context}

Answer:"""

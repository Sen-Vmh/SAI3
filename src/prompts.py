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

#FOR THE QUESTIONS, DONT CHANGE OR DELETE PLS
SUGGEST_QUESTIONS_SYSTEM_PROMPT = (
    "You are a financial advisor. "
    "Your only job is to generate short, specific questions a user should ask "
    "based on weaknesses in their portfolio. "
    "The questions must be answerable using these books: "
    "A Random Walk Down Wall Street, Markowitz Portfolio Selection, "
    "Fama Efficient Market Hypothesis, The Elements of Investing, Principles of Finance."
)

SUGGEST_QUESTIONS_USER_PROMPT = """Based on this portfolio summary, generate exactly 4 short questions the user should ask to improve their portfolio.

Rules:
- Each question must target a specific weakness or gap in the portfolio
- Keep each question under 15 words
- Return only the 4 questions, one per line, no numbering, no explanation

Portfolio summary:
{survey_summary}

Questions:"""

"""
Type 1: Document Loading RAG

The simplest form of RAG. Load entire documents into the prompt.
No database, no embeddings, no chunking. Just files in a prompt.

Best for: Small document sets, policy docs, FAQs, runbooks.
Run: uv run src/01_document_loading.py
"""

from openai import OpenAI
from pathlib import Path

client = OpenAI()

DATA_DIR = Path(__file__).parent.parent / "data"


def load_documents() -> str:
    """Load all documents from the data directory."""
    docs = []
    for filepath in sorted(DATA_DIR.glob("*.md")):
        content = filepath.read_text()
        docs.append(f"--- {filepath.name} ---\n{content}")
    return "\n\n".join(docs)


def ask(question: str) -> str:
    """Load all documents and ask a question."""
    context = load_documents()

    response = client.responses.create(
        model="gpt-5.4",
        instructions="You are a helpful support agent for ShopMax, an online shoe store. Use the provided documents to answer questions accurately. If the answer is not in the documents, say so.",
        input=f"Documents:\n{context}\n\nQuestion: {question}",
    )
    return response.output_text


if __name__ == "__main__":
    questions = [
        "What's your return policy for opened items?",
        "How long does shipping take?",
        "Can I get a refund if I wore the shoes outside?",
    ]

    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {ask(q)}")
        print("-" * 60)

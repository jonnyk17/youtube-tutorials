"""
Type 5: SQL RAG

The LLM generates SQL from natural language. No embeddings needed.
When your data has structure (price, rating, brand), just query it.

Best for: Structured data with exact filters, aggregations, sorting.
Breaks when: Users ask about unstructured attributes ("comfortable", "stylish").
Run: uv run src/05_sql_rag.py
"""

import os
from openai import OpenAI
import psycopg
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
DATABASE_URL = os.environ["DATABASE_URL"]

SCHEMA = """
Table: products
Columns:
  - id: SERIAL PRIMARY KEY
  - name: TEXT (product name)
  - brand: TEXT (Nike, Adidas, Asics, Salomon, New Balance)
  - category: TEXT (running, casual, hiking, training)
  - price: DECIMAL (in USD)
  - rating: DECIMAL (1.0 to 5.0)
  - color: TEXT
  - description: TEXT
""".strip()


def generate_sql(question: str) -> str:
    """Use GPT-5.4 to generate a SQL query from natural language."""
    response = client.responses.create(
        model="gpt-5.4",
        instructions=f"""You are a SQL expert. Generate a PostgreSQL SELECT query based on the user's question.

Database schema:
{SCHEMA}

Rules:
- Return ONLY the SQL query, no explanation, no markdown.
- Always use SELECT (never INSERT, UPDATE, DELETE, DROP, etc.).
- Use ILIKE for text matching when appropriate.
- Limit results to 10 unless the user asks for more.""",
        input=question,
    )
    return response.output_text.strip()


def execute_query(sql: str) -> list[dict]:
    """Execute a SQL query and return results as dicts."""
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            columns = [desc[0] for desc in cur.description]
            results = [dict(zip(columns, row)) for row in cur.fetchall()]
    return results


def ask(question: str) -> str:
    """Generate SQL, execute it, and answer with GPT-5.4."""
    sql = generate_sql(question)
    print(f"  Generated SQL: {sql}")

    results = execute_query(sql)

    if not results:
        context = "The query returned no results."
    else:
        context = "\n".join(str(r) for r in results)

    response = client.responses.create(
        model="gpt-5.4",
        instructions="You are a helpful shopping assistant for ShopMax. Answer the customer's question based on the query results. Be specific about prices and ratings.",
        input=f"Query results:\n{context}\n\nOriginal question: {question}",
    )
    return response.output_text


if __name__ == "__main__":
    # This works perfectly: structured filters
    print("=" * 60)
    print("QUERY: 'Show me running shoes under $100 with at least 4 stars'")
    print("=" * 60)
    answer = ask("Show me running shoes under $100 with at least 4 stars, sorted by price")
    print(f"\nA: {answer}")

    print("\n" + "=" * 60)
    print("QUERY: 'What is the cheapest product you have?'")
    print("=" * 60)
    answer = ask("What is the cheapest product you have?")
    print(f"\nA: {answer}")

    print("\n" + "=" * 60)
    print("QUERY: 'How many Nike products do you carry?'")
    print("=" * 60)
    answer = ask("How many Nike products do you carry?")
    print(f"\nA: {answer}")

    # This breaks: unstructured questions
    print("\n" + "=" * 60)
    print("QUERY: 'Find me something good for trail running in wet conditions'")
    print("=" * 60)
    answer = ask("Find me something good for trail running in wet conditions")
    print(f"\nA: {answer}")
    print("\n  ^ SQL can't understand 'wet conditions'. There's no 'wetness' column.")

"""
Type 6: Agentic RAG

The agent picks the right retrieval strategy based on the question.
It has tools for all five previous approaches and decides which to use.

Best for: Complex questions that span structured and unstructured data.
Run: uv run src/06_agentic_rag.py
"""

import os
import json
from openai import OpenAI
import psycopg
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
DATABASE_URL = os.environ["DATABASE_URL"]
DATA_DIR = Path(__file__).parent.parent / "data"

PRODUCT_SCHEMA = """
Table: products
Columns: id, name (TEXT), brand (TEXT), category (TEXT), price (DECIMAL), rating (DECIMAL 1-5), color (TEXT), description (TEXT)
Brands: Nike, Adidas, Asics, Salomon, New Balance
Categories: running, casual, hiking, training
""".strip()

# --- Tool implementations ---


def embed(text: str) -> list[float]:
    """Embed a single text using OpenAI."""
    response = client.embeddings.create(model="text-embedding-3-small", input=[text])
    return response.data[0].embedding


def load_document(filename: str) -> str:
    """Load a document from the data directory."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        available = [f.name for f in DATA_DIR.glob("*.md")]
        return f"File '{filename}' not found. Available: {available}"
    return filepath.read_text()


def full_text_search(query: str) -> str:
    """Keyword search on product descriptions."""
    conn = psycopg.connect(DATABASE_URL)
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT name, brand, price, rating, description
            FROM products
            WHERE description_tsv @@ websearch_to_tsquery('english', %s)
            ORDER BY ts_rank(description_tsv, websearch_to_tsquery('english', %s)) DESC
            LIMIT 5
            """,
            (query, query),
        )
        results = cur.fetchall()
    conn.close()

    if not results:
        return "No keyword matches found."
    return "\n".join(
        f"- {r[0]} ({r[1]}) ${r[2]} {r[3]}★: {r[4]}" for r in results
    )


def vector_search(query: str) -> str:
    """Semantic search on product descriptions."""
    query_embedding = embed(query)

    conn = psycopg.connect(DATABASE_URL)
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT name, brand, price, rating, description
            FROM products
            ORDER BY embedding <=> %s::vector
            LIMIT 5
            """,
            (str(query_embedding),),
        )
        results = cur.fetchall()
    conn.close()

    return "\n".join(
        f"- {r[0]} ({r[1]}) ${r[2]} {r[3]}★: {r[4]}" for r in results
    )


def sql_query(query: str) -> str:
    """Execute a SQL query against the products table."""
    conn = psycopg.connect(DATABASE_URL)
    with conn.cursor() as cur:
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        results = [dict(zip(columns, row)) for row in cur.fetchall()]
    conn.close()
    return json.dumps(results, default=str) if results else "No results."


# --- Tool definitions for OpenAI function calling ---

TOOLS = [
    {
        "type": "function",
        "name": "load_document",
        "description": "Load an entire document file. Use for policy questions, FAQs, or when you need the full document. Available files: faq.md, refund-policy.md",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The filename to load (e.g. 'faq.md', 'refund-policy.md')",
                }
            },
            "required": ["filename"],
        },
    },
    {
        "type": "function",
        "name": "full_text_search",
        "description": "Keyword search on product descriptions. Use when the user mentions specific words, brand names, or features they want to match exactly.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The keyword search query",
                }
            },
            "required": ["query"],
        },
    },
    {
        "type": "function",
        "name": "vector_search",
        "description": "Semantic search on product descriptions. Use when the user describes what they want in natural language and you need to find similar products by meaning.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Natural language description of what to search for",
                }
            },
            "required": ["query"],
        },
    },
    {
        "type": "function",
        "name": "sql_query",
        "description": f"Execute a SQL SELECT query on the products table. Use for exact filters on price, rating, brand, category, or color. Schema: {PRODUCT_SCHEMA}",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A PostgreSQL SELECT query",
                }
            },
            "required": ["query"],
        },
    },
]

TOOL_HANDLERS = {
    "load_document": lambda args: load_document(args["filename"]),
    "full_text_search": lambda args: full_text_search(args["query"]),
    "vector_search": lambda args: vector_search(args["query"]),
    "sql_query": lambda args: sql_query(args["query"]),
}


def ask(question: str) -> str:
    """Run the agentic RAG loop. The agent picks which tools to use."""
    print(f"\n{'=' * 60}")
    print(f"Q: {question}")
    print("=" * 60)

    response = client.responses.create(
        model="gpt-5.4",
        instructions="You are a helpful shopping assistant for ShopMax. Use the available tools to find the best information to answer the customer's question. You can use multiple tools if the question has multiple parts.",
        input=question,
        tools=TOOLS,
    )

    # Process tool calls in a loop
    while response.output:
        has_tool_calls = any(
            item.type == "function_call" for item in response.output
        )
        if not has_tool_calls:
            break

        # Collect tool results
        tool_results = []
        for item in response.output:
            if item.type == "function_call":
                tool_name = item.name
                tool_args = json.loads(item.arguments)
                print(f"  Tool: {tool_name}({json.dumps(tool_args)})")

                result = TOOL_HANDLERS[tool_name](tool_args)
                tool_results.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": result,
                    }
                )

        # Continue the conversation with tool results
        response = client.responses.create(
            model="gpt-5.4",
            previous_response_id=response.id,
            input=tool_results,
            tools=TOOLS,
        )

    # Extract final text
    for item in response.output:
        if item.type == "message":
            for content in item.content:
                if content.type == "output_text":
                    return content.text

    return "No response generated."


if __name__ == "__main__":
    # Compound question: needs SQL + document loading
    answer = ask(
        "I want running shoes under $150 but what's your return policy if they don't fit?"
    )
    print(f"\nA: {answer}")

    # Needs vector search: semantic understanding
    answer = ask("What shoes are best for running in the rain?")
    print(f"\nA: {answer}")

    # Needs SQL: exact structured query
    answer = ask("What's the highest rated shoe you have?")
    print(f"\nA: {answer}")

    # Needs multiple tools: keyword + document
    answer = ask(
        "Do you have any Salomon shoes? And can I return them if I use them on a trail?"
    )
    print(f"\nA: {answer}")

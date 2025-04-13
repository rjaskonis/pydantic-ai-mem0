import os
from dotenv import load_dotenv

load_dotenv(override=True)

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
PGVECTOR_HOST = os.environ["PGVECTOR_HOST"]
PGVECTOR_PORT = os.environ["PGVECTOR_PORT"]
PGVECTOR_USER = os.environ["PGVECTOR_USER"]
PGVECTOR_PASSWORD = os.environ["PGVECTOR_PASSWORD"]

config = {
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "gpt-4o-mini"
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-small"
        }
    },
    "vector_store": {
        "provider": "pgvector",
        "config": {
            "host": PGVECTOR_HOST,
            "port": PGVECTOR_PORT,
            "user": PGVECTOR_USER,
            "password": PGVECTOR_PASSWORD,
        }
    }
}
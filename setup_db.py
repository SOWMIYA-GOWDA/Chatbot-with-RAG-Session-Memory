#!/usr/bin/env python3
"""Setup script to build the vector database"""

from backend.rag import build_vector_db

if __name__ == "__main__":
    print("🔨 Building vector database...")
    db = build_vector_db()
    print("✅ Vector database built successfully!")

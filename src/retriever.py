
from pathlib import Path
import hashlib

import chromadb
from sentence_transformers import SentenceTransformer


class DocumentRetriever:
    def __init__(self, db_path="chroma_db"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="internal_documents"
        )

    def index_documents(self, docs_folder="docs"):
        """Read, split, and index Markdown documents."""

        documents = []
        chunk_ids = []
        metadata = []

        for file_path in Path(docs_folder).glob("*.md"):
            content = file_path.read_text(encoding="utf-8")

            # Create overlapping chunks of approximately 250 words.
            words = content.split()
            chunk_size = 250
            overlap = 50
            step = chunk_size - overlap

            for start in range(0, len(words), step):
                chunk = " ".join(words[start:start + chunk_size])

                if not chunk:
                    continue

                unique_key = f"{file_path.name}:{start}:{chunk}"
                chunk_id = hashlib.sha256(
                    unique_key.encode("utf-8")
                ).hexdigest()[:16]

                documents.append(chunk)
                chunk_ids.append(chunk_id)
                metadata.append({
                    "filename": file_path.name,
                    "start_word": start,
                })

        if not documents:
            return 0

        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True
        ).tolist()

        self.collection.upsert(
            ids=chunk_ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadata,
        )

        return len(documents)

    def retrieve(self, query: str, k: int = 20):
        """Retrieve the closest document chunks."""

        if not query.strip() or self.collection.count() == 0:
            return []

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        ).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=min(k, self.collection.count()),
            include=["documents", "distances", "metadatas"],
        )

        candidates = []

        for chunk_id, content, distance, metadata in zip(
            results["ids"][0],
            results["documents"][0],
            results["distances"][0],
            results["metadatas"][0],
        ):
            candidates.append({
                "chunk_id": chunk_id,
                "content": content,
                "distance": distance,
                "filename": metadata["filename"],
                "source": "internal_doc",
            })

        return candidates

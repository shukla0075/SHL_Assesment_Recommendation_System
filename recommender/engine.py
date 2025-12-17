import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


class SHLRecommender:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.read_index("embeddings/shl.faiss")
        self.meta = pd.read_csv("data/processed/shl_metadata.csv")

    def extract_skills(self, query):
        skills = [
            "python", "java", "sql", "javascript",
            "communication", "teamwork", "leadership",
            "problem solving", "analysis"
        ]
        found = [s for s in skills if s.lower() in query.lower()]
        return " ".join(found)

    def enrich_query(self, query):
        skills = self.extract_skills(query)
        return (
            f"{query}. "
            f"Skills: {skills}. "
            f"Technical assessment. "
            f"Behavioral assessment."
        )

    def recommend(self, query, k=10):
        enriched_query = self.enrich_query(query)
        q_emb = self.model.encode([enriched_query])

        # search more candidates for better balancing
        _, idx = self.index.search(np.array(q_emb), k * 3)

        results = self.meta.iloc[idx[0]].to_dict(orient="records")

        k_tests = [r for r in results if "K" in r["test_type"]]
        p_tests = [r for r in results if "P" in r["test_type"]]
        others = [r for r in results if r not in k_tests + p_tests]

        final = []
        final.extend(k_tests[:k // 2])
        final.extend(p_tests[:k // 2])
        final.extend(others)

        return final[:k]

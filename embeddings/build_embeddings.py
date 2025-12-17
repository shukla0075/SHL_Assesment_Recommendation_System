import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

df = pd.read_csv("data/raw/shl_catalog.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = (
    df["name"] + " " +
    df["description"] + " " +
    df["test_type"]
).tolist()

embeddings = model.encode(texts, show_progress_bar=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

faiss.write_index(index, "embeddings/shl.faiss")
df.to_csv("data/processed/shl_metadata.csv", index=False)

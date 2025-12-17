import pandas as pd
from recommender.engine import SHLRecommender

K = 10

def mean_recall_at_k():
    df = pd.read_excel("data/labelled_train.xlsx")
    recommender = SHLRecommender()
    recalls = []

    for query, group in df.groupby("Query"):
        gt = set(group["Assessment_url"])
        preds = recommender.recommend(query, K)
        pred_urls = set(p["url"] for p in preds)

        recall = len(gt & pred_urls) / len(gt)
        recalls.append(recall)

    return sum(recalls) / len(recalls)

if __name__ == "__main__":
    print("Mean Recall@10:", mean_recall_at_k())

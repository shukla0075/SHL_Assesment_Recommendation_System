# SHL Assessment Recommendation System

This project implements an end-to-end recommendation system that suggests relevant SHL assessments based on natural-language hiring requirements. The system crawls the SHL Product Catalog, builds semantic embeddings for assessments, retrieves relevant assessments using vector similarity search, and evaluates performance using Recall@K.

The implementation strictly follows the requirements outlined in the **SHL AI Intern – Generative AI Assignment**.

---

## Problem Statement

Given a hiring requirement written in natural language (for example:  
“Looking for a Python developer with SQL and teamwork skills”), the goal is to recommend the most relevant assessments from the SHL Product Catalog.

---

## Solution Overview

The solution consists of the following stages:

1. Crawling SHL Individual Test Solutions
2. Building semantic embeddings for assessments
3. Performing vector-based retrieval using FAISS
4. Evaluating recommendations using a labelled dataset
5. Exposing the system via a local web application

---

## Project Structure

```

shl_recommender/
│
├── crawler/
│   └── crawl_shl.py
│
├── embeddings/
│   ├── build_embeddings.py
│   └── shl.faiss
│
├── recommender/
│   └── engine.py
│
├── evaluation/
│   └── evaluate.py
│
├── api/
│   └── main.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── labelled_train.xlsx
│
├── requirements.txt
└── README.md

````

---

## Setup Instructions

### Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
````

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Crawling SHL Product Catalog

The crawler extracts **Individual Test Solutions** from the SHL Product Catalog and handles pagination automatically.

```bash
python crawler/crawl_shl.py
```

Output file:

```
data/raw/shl_catalog.csv
```

Total assessments crawled: **377**

---

## Embedding Generation and Indexing

Each assessment is represented using its metadata and embedded using a sentence-transformer model.

* Embedding model: `all-MiniLM-L6-v2`
* Vector index: FAISS (cosine similarity)

To build embeddings:

```bash
python embeddings/build_embeddings.py
```

Outputs:

* `embeddings/shl.faiss`
* `data/processed/shl_metadata.csv`

---

## Recommendation Engine

The recommendation engine performs the following steps:

* Enriches the input query with assessment-related context
* Converts the query into a semantic embedding
* Retrieves top candidates using FAISS
* Balances results across:

  * Technical / Knowledge tests (K)
  * Personality / Behavioral tests (P)
  * Other assessment types

Example usage:

```python
from recommender.engine import SHLRecommender

recommender = SHLRecommender()
results = recommender.recommend(
    "Python developer with SQL and teamwork skills",
    k=10
)
```

---

## Evaluation

Evaluation is performed using the provided labelled dataset:

```
data/labelled_train.xlsx
```

Metric used:

* **Recall@10**

Run evaluation:

```bash
python -m evaluation.evaluate
```

The evaluation computes recall based on URL-level matches between recommended assessments and ground truth.

---

## Local Web Application

A local web interface is provided to demonstrate the system.

### Run the Application

```bash
uvicorn api.main:app --reload
```

### Open in Browser

```
http://127.0.0.1:8000
```

Users can input hiring requirements and view recommended SHL assessments in real time.

---

## Observations and Limitations

* Recall values are modest due to:

  * Small labelled dataset
  * Exact URL-based evaluation
  * Use of a general-purpose embedding model
* Despite this, the system demonstrates:

  * Correct semantic retrieval
  * Balanced recommendation logic
  * End-to-end reproducibility

---

## Future Improvements

* Domain-specific embedding fine-tuning
* Hybrid keyword and semantic ranking
* Learning-to-rank using labelled data
* Advanced skill extraction techniques

---

## Author

Developed as part of the **SHL AI Intern – Generative AI Assignment**.

```

---

If you want, next I can:
- Verify this README line-by-line against the PDF  
- Help you write a **short submission explanation**
- Prepare **what to say if recall is questioned**

Just tell me 👍
```

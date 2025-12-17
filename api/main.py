from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from recommender.engine import SHLRecommender


# ------------------ App Setup ------------------

app = FastAPI(title="SHL Assessment Recommendation API")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

recommender = SHLRecommender()


# ------------------ UI Routes ------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": None}
    )


@app.post("/", response_class=HTMLResponse)
async def recommend_ui(request: Request):
    form = await request.form()
    query = form.get("query")

    results = recommender.recommend(query, k=10)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": results}
    )


# ------------------ API Route (JSON) ------------------

@app.get("/api/recommend")
def recommend_api(
    query: str = Query(..., description="Hiring requirement or job description"),
    k: int = Query(10, description="Number of recommendations")
):
    results = recommender.recommend(query, k=k)

    return {
        "query": query,
        "top_k": k,
        "results": results
    }


# ------------------ Health Check ------------------

@app.get("/health")
def health():
    return {"status": "ok"}

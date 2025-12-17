from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from recommender.engine import SHLRecommender
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

recommender = SHLRecommender()


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


@app.get("/health")
def health():
    return {"status": "ok"}

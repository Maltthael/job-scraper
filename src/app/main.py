import sys
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import vagas

@asynccontextmanager
async def lifespan(app: FastAPI):
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    yield

app = FastAPI(title="Job Scraper API", lifespan=lifespan)

app.include_router(vagas.router)

@app.get("/")
def health_check():
    return {"status": "ok", "mensagem": "API de Vagas rodando!"}
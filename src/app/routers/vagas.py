from fastapi import APIRouter, Query
from typing import List, Optional
from app.services.remota_service import buscar_remotar_playwright
from app.services.gupy_service import buscar_gupy_playwright
from pydantic import BaseModel
import asyncio

router = APIRouter(prefix="/api/vagas", tags=["Vagas"])

class VagaSchema(BaseModel):
    titulo: str
    empresa: str
    link: str
    fonte: str
    
class RespostaVagasSchema(BaseModel):
    total: int
    vagas: List[VagaSchema]

@router.get("/", response_model=RespostaVagasSchema)
async def obter_vagas(
    termo: str = Query(default="estagio", description="Termo de busca para as vagas")
):
    """
    Busca vagas em paralelo nos portais Remotar e Gupy.
    """

    resultados = await asyncio.gather(
        buscar_remotar_playwright(),
        buscar_gupy_playwright(termo),
        return_exceptions=True 
    )

    todas_vagas = []

    for res in resultados:
        if isinstance(res, list):
            todas_vagas.extend(res)
        elif isinstance(res, Exception):
            print(f"[Erro no Scraper]: {res}")

    return {
        "total": len(todas_vagas),
        "vagas": todas_vagas
    }
    



@router.get("/gupy", response_model=RespostaVagasSchema)
async def obter_vagas_gupy(
    termo: str = Query(default="estagio", description="Termo de busca para o Gupy")
):
    """Busca vagas exclusivamente no portal Gupy."""
    vagas = await buscar_gupy_playwright(termo)

    return {
        "total": len(vagas),
        "vagas": vagas
    }
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import pandas as pd
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajuste para seu domínio depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def ler_planilha_csv(caminho: str) -> List[dict]:
    df = pd.read_csv(caminho, encoding="latin1", sep=';', dtype={'COD. BARRAS': str})
    return df.to_dict(orient="records")

@app.get("/")
def root():
    return {"mensagem": "API da planilha CSV está rodando!"}

@app.get("/api/dados")
def get_dados():
    caminho = os.path.abspath("planilha.csv")
    if not os.path.exists(caminho):
        return {"erro": f"Arquivo não encontrado em: {caminho}"}
    try:
        dados = ler_planilha_csv(caminho)
        return dados
    except Exception as e:
        return {"erro": str(e)}


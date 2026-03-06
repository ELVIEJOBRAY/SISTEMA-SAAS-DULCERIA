from fastapi import FastAPI

app = FastAPI(
    title="SGDD API",
    description="Sistema de Gestión de Dulcerías SaaS",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "🚀 SGDD API funcionando correctamente"}

@app.get("/health")
def health():
    return {"status": "ok", "message": "Sistema operativo"}

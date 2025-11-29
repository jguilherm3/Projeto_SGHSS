from fastapi import FastAPI
from .database import engine, Base
from .routers import auth_router, pacientes_router, consultas_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SGHSS VidaPlus API",
    description="API para o Sistema de Gestão Hospitalar e de Serviços de Saúde",
    version="1.0.0"
)

app.include_router(auth_router.router)
app.include_router(pacientes_router.router)
app.include_router(consultas_router.router)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API SGHSS VidaPlus está online! Acesse /docs para documentação."}
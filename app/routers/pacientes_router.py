from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud, models, auth
from ..database import get_db

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)

# Rota: Meu Perfil (GET /pacientes/me)

@router.get("/me", response_model=schemas.Paciente)
def read_paciente_me(
    current_user_email: str = Depends(auth.get_current_user), # Exige Login!
    db: Session = Depends(get_db)
):
    """
    Retorna os dados do paciente logado.
    O sistema identifica o paciente pelo Token JWT (email).
    """
    # 1. Busca o usuário pelo email do token
    usuario = crud.get_usuario_by_email(db, email=current_user_email)
    
    # 2. Verifica se encontrou e se é um paciente
    if not usuario or not usuario.paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Paciente não encontrado ou perfil incorreto."
        )
        
    return usuario.paciente
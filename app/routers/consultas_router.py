from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud, models, auth
from ..database import get_db

router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"]
)

# Rota: Agendar Consulta (POST /consultas)

@router.post("/", response_model=schemas.Consulta)
def agendar_consulta(
    consulta: schemas.ConsultaCreate, 
    current_user_email: str = Depends(auth.get_current_user), # Exige Login
    db: Session = Depends(get_db)
):
    """
    Paciente agenda uma nova consulta.
    O ID do paciente é obtido automaticamente do usuário logado.
    """
    # 1. Identifica quem está logado
    usuario = crud.get_usuario_by_email(db, email=current_user_email)
    
    if not usuario or not usuario.paciente:
         raise HTTPException(status_code=400, detail="Apenas pacientes podem agendar consultas.")

    # 2. Força o ID do paciente para ser o do usuário logado (Segurança)
    # (Mesmo que o JSON traga outro ID, usamos o do token)
    consulta.paciente_id = usuario.paciente.id
    
    # 3. Chama o CRUD para criar
    return crud.create_consulta(db=db, consulta=consulta)

# Rota: Minhas Consultas (GET /consultas/minhas)

@router.get("/minhas", response_model=List[schemas.Consulta])
def listar_minhas_consultas(
    current_user_email: str = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as consultas do paciente (ou médico) logado.
    """
    usuario = crud.get_usuario_by_email(db, email=current_user_email)
    
    if usuario.perfil == 'paciente':
        return crud.get_consultas_by_paciente_id(db, paciente_id=usuario.paciente.id)
    elif usuario.perfil == 'profissional':
        return crud.get_consultas_by_profissional_id(db, profissional_id=usuario.profissional.id)
    else:
        return []
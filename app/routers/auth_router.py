# Este é o 'app/routers/auth_router.py'

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import schemas, crud, models, auth
from ..database import get_db

router = APIRouter(
    prefix="/auth",  # Todas as rotas aqui começarão com /auth
    tags=["Autenticação"] # Agrupa no Swagger/docs
)

# ---------------------------------------------------------------
# Rota de Registro de Paciente
# ---------------------------------------------------------------
@router.post("/register/paciente", response_model=schemas.Paciente)
def register_paciente(
    registro_data: schemas.RegistroPacienteCreate, 
    db: Session = Depends(get_db)
):
    """
    Endpoint para registrar um novo paciente e seu usuário associado.
    """
    # Verifica se o email já existe no banco
    db_usuario = crud.get_usuario_by_email(db, email=registro_data.usuario_data.email)
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado."
        )
    
    # Se não existe, chama a função do crud para criar o paciente e o usuário
    try:
        paciente_criado = crud.create_paciente(db=db, registro_data=registro_data)
        return paciente_criado
    except Exception as e:
        # Captura erros gerais (ex: CPF duplicado, se o banco travar)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar paciente: {str(e)}"
        )

# ---------------------------------------------------------------
# Rota de Login (Token) - Conforme o PDF
# ---------------------------------------------------------------
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Endpoint de login. Recebe 'username' (que é o email) e 'password'.
    Retorna um token JWT.
    """
    # 1. Busca o usuário pelo email (username no formulário)
    user = crud.get_usuario_by_email(db, email=form_data.username)

    # 2. Verifica se o usuário existe E se a senha está correta
    if not user or not auth.verificar_senha(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Se deu certo, cria o token JWT
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "perfil": user.perfil}, 
        expires_delta=access_token_expires
    )
    
    # 4. Retorna o token no formato { "access_token": "...", "token_type": "bearer" }
    return {"access_token": access_token, "token_type": "bearer"}
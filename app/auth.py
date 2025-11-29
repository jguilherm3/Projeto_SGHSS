from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional


# 1. Hashing de Senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Configuração JWT (Token)
# rodar: python -c 'import secrets; print(secrets.token_hex(32))'
SECRET_KEY = "fb6b4d233d37e89f8f42e1a425d04e682281c7cc2e65606919ae40b8efe87b30"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #token expira em 30 minutos

# Isso diz ao FastAPI que os tokens devem ser buscados na rota /auth/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifica se a senha plana corresponde ao hash armazenado."""
    return pwd_context.verify(senha_plana, senha_hash)

def get_hash_senha(senha: str) -> str:
    """Gera um hash bcrypt para a senha."""
    return pwd_context.hash(senha)


# Funções de Token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um novo token de acesso JWT."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[str]:
    """Decodifica o token e retorna o 'sub' (email/id) se for válido."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 'sub'='subject' é o identificador se coloca no token
        sub: str = payload.get("sub") 
        if sub is None:
            return None
        return sub
    except JWTError:
        return None

# Dependência de Autenticação

async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependência do FastAPI para proteger rotas.
    Verifica o token e retorna o 'subject' (email) do usuário.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = decode_token(token)
    
    if email is None:
        raise credentials_exception
    # Por enquanto, retornar o email é suficiente para identificação.
    return email
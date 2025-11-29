from sqlalchemy.orm import Session
from . import models, schemas, auth
from typing import List


# CRUD de Usuário

def get_usuario_by_email(db: Session, email: str) -> models.Usuario:
    """Busca um usuário no banco de dados pelo email."""
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate) -> models.Usuario:
    """Cria um novo registro de usuário no banco."""
    
    # Pega a senha em texto plano e gera o hash
    hashed_password = auth.get_hash_senha(usuario.senha)
    
    # Cria o objeto do modelo SQLAlchemy
    db_usuario = models.Usuario(
        email=usuario.email, 
        senha_hash=hashed_password, 
        perfil=usuario.perfil
    )
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario) # Atualiza o db_usuario com o ID gerado pelo banco
    return db_usuario

# CRUD de Paciente

def create_paciente(db: Session, registro_data: schemas.RegistroPacienteCreate) -> models.Paciente:
    """
    Cria um novo Paciente e seu respectivo Usuário em uma transação.
    Usa o schema composto 'RegistroPacienteCreate'.
    """
    
    # 1. Cria o objeto Usuario
    usuario_data = registro_data.usuario_data
    hashed_password = auth.get_hash_senha(usuario_data.senha)
    
    db_usuario = models.Usuario(
        email=usuario_data.email,
        senha_hash=hashed_password,
        perfil="paciente" # Força o perfil para 'paciente'
    )
    
    db.add(db_usuario)
    db.commit() # Faz o commit para que o db_usuario receba um ID
    db.refresh(db_usuario)
    
    # 2. Cria o objeto Paciente, linkando ao usuário recém-criado
    paciente_data = registro_data.paciente_data
    db_paciente = models.Paciente(
        **paciente_data.model_dump(), # Desempacota os dados (nome, cpf, etc)
        usuario_id=db_usuario.id      # Linka com o ID do usuário
    )
    
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    
    return db_paciente # Retorna o paciente completo

def get_paciente_by_id(db: Session, paciente_id: int) -> models.Paciente:
    """Busca um paciente pelo seu ID."""
    return db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()

# ---------------------------------------------------------------
# TODO: Funções CRUD de Profissional
# ---------------------------------------------------------------

def create_profissional(db: Session, registro_data: schemas.RegistroProfissionalCreate) -> models.Profissional:
    """Cria um novo registro de usuário no banco"""  
    
    usuario_data = registro_data.usuario_data
    hashed_password = auth.get_hash_senha(usuario_data.senha)

    db_usuario = models.Usuario(
        email=usuario_data.email,
        senha_hash=hashed_password,
        perfil="profissional"
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    profissional_data = registro_data.profissional_data
    db_profissional = models.Profissional(
        **profissional_data.model_dump(), # Desempacota os dados
        usuario_id=db_usuario.id # Vai linka com o ID do usuário
    )

    db.add(db_profissional)
    db.commit()
    db.refresh(db_profissional)

    return db_profissional

def get_profissional_by_id(db: Session, profissional_id: int) -> models.Profissional:
    return db.query(models.Profissional).filter(models.Profissional.id == profissional_id).first()

# ---------------------------------------------------------------
# TODO: Funções CRUD de Consulta
# ---------------------------------------------------------------

def create_consulta(db: Session, consulta: schemas.ConsultaCreate) -> models.Consulta:
    
    db_consulta = models.Consulta(**consulta.model_dump())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)

    return db_consulta

def get_consultas_by_paciente_id(db: Session, paciente_id: int) -> List[models.Consulta]:
    return db.query(models.Consulta).filter(models.Consulta.paciente_id == paciente_id).all()

def get_consultas_by_profissional_id(db: Session, profissional_id: int) -> List[models.Consulta]:
    return db.query(models.Consulta).filter(models.Consulta.profissional_id == profissional_id).all()
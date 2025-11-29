from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UsuarioBase(BaseModel):
    email: EmailStr
    perfil: str


class UsuarioCreate(UsuarioBase):
    senha: str


class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True # Permite que o Pydantic leia o modelo sqlalchemy

# schema do prontuário
class ProntuarioBase(BaseModel):
    descricao_atendimento : str
    receitas_emitidas : Optional[str] = None


class ProntuarioCreate(ProntuarioBase):
    pass


class Prontuario(ProntuarioBase):
    id: int
    consulta_id: int

    class Config:
        from_attributes = True

# schema da consulta
class ConsultaBase(BaseModel):
    data_hora: datetime
    status: Optional[str] = "agendada"
    tipo: Optional[str] = "presencial"


# schema que vai criar uma consulta
class ConsultaCreate(ConsultaBase):
    paciente_id: Optional[int] = None
    profissional_id: int


# schema para ler uma consulta
class Consulta(ConsultaBase):
    id: int
    paciente_id: int
    profissional_id: int
    prontuario: Optional[Prontuario] = None # relacionamento aninhado

    class Config:
        from_attributes = True


# schema do paciente
class PacienteBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: datetime
    telefone: Optional[str] = None

class PacienteCreate(PacienteBase):
    pass


# Schema para ler um paciente
class Paciente(PacienteBase):
    id: int
    usuario_id: int
    usuario: Usuario
    consultas: List[Consulta] = []

    class Config:
        from_attributes = True


# Schemas do Profissional
class ProfissionalBase(BaseModel):
    nome: str
    crm: str
    especialidade: Optional[str] = None

class ProfissionalCreate(ProfissionalBase):
    pass

# Schema para ler um profissional (mostra o usuário e suas consultas)
class Profissional(ProfissionalBase):
    id: int
    usuario_id: int
    usuario: Usuario               # Relacionamento aninhado
    consultas: List[Consulta] = [] # Relacionamento aninhado

    class Config:
        from_attributes = True


# Schema Composto (Especial para Registro)
# Este schema facilita a rota de registro, recebendo
# os dados do usuário e do paciente de uma só vez.
class RegistroPacienteCreate(BaseModel):
    usuario_data: UsuarioCreate
    paciente_data: PacienteCreate

class RegistroProfissionalCreate(BaseModel):
    usuario_data: UsuarioCreate
    profissional_data: ProfissionalCreate

class Token(BaseModel):
    access_token : str
    token_type: str
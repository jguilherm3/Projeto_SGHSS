from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash=Column(String, nullable=False)
    perfil= Column(String, nullable=False) # 'paciente', 'profissionnal', 'admin'

    paciente = relationship("Paciente", back_populates='usuario', uselist=False)
    profissional = relationship("Profissional", back_populates="usuario", uselist=False)


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    data_nascimento = Column(DateTime, nullable=False)
    telefone = Column(String)

    # Chave Estrangeira: Liga o Paciente ao seu registro de Usuário
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)

    # "back_populates" cria o link de volta para o Usuario
    usuario = relationship("Usuario", back_populates="paciente")

    # relacionamento um-para-muitos
    consultas = relationship("Consulta", back_populates="paciente")


class Profissional(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    crm = Column(String, unique=True, index=True, nullable=False)
    especialidade = Column(String)

    #foreign key: liga o profissional ao seu registro de usuário
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)

    # relacionamento
    usuario = relationship("Usuario", back_populates="profissional")

    # um profissional para muitas consultas
    consultas = relationship("Consulta", back_populates="profissional")


class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, nullable=False, index=True)
    status = Column(String, default="agendada") # Ex: 'agendada', 'realizada', 'cancelada'
    tipo = Column(String, default="presencial")# Ex: 'presencial', 'telemedicina'

    ## chaves estrangeiras
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    profissional_id=Column(Integer, ForeignKey("profissionais.id"), nullable=False)

    #relacionamentos
    paciente = relationship("Paciente", back_populates="consultas")
    profissional = relationship("Profissional", back_populates="consultas")

    # Relacionamento um-para-um
    # "uma consulta tem um prontuário"
    prontuario = relationship("Prontuario", back_populates="consulta", uselist=False)


class Prontuario(Base):
    __tablename__ = "prontuarios"

    id = Column(Integer, primary_key=True, index=True)
    descricao_atendimento = Column(Text, nullable=False)
    receitas_emitidas = Column(Text)

    # chave estrangeira um-para-um
    consulta_id = Column(Integer, ForeignKey("consultas.id"), unique=True, nullable=False)

    #relacionamentos
    consulta = relationship("Consulta", back_populates="prontuario")
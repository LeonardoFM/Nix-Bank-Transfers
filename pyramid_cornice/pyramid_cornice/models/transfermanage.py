from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Table,
    ForeignKey
)
from sqlalchemy.orm import relationship

from .meta import Base

# Model relationship between clients and its bank transfers
#
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#one-to-one
class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    transfers = relationship("Transfers", back_populates="client")
    nome = Column(Text)
    cnpj = Column(Text)


class Transfers(Base):
    __tablename__ = 'transfers'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    client = relationship("Client",uselist=False, back_populates="transfers")
    pagador_nome = Column(Text)
    pagador_banco = Column(Text)
    pagador_agencia = Column(Text)
    pagador_conta = Column(Text)
    beneficiario_nome = Column(Text)
    beneficiario_banco = Column(Text)
    beneficiario_agencia = Column(Text)
    beneficiario_conta = Column(Text)
    valor = Column(Integer)
    tipo = Column(Text) # (CC,TED,DOC)
    status = Column(Text) # (OK, ERRO)

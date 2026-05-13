from pydantic import BaseModel


class ClienteCreate(BaseModel):
    """Payload para criação de um cliente."""

    cpf: str
    nome: str = ""


class ClienteOut(BaseModel):
    """Dados de retorno de um cliente."""

    cpf: str
    nome: str = ""


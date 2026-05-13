from dataclasses import dataclass


@dataclass(frozen=True)
class Cliente:
    """Representa um cliente da lanchonete.

    Imutável (frozen=True): uma vez criado, CPF e nome não podem ser alterados.

    Attributes:
        cpf: CPF do cliente, usado como identificador único.
        nome: Nome do cliente (opcional).
    """

    cpf: str
    nome: str = ""
````markdown
# API de Reserva de Salas de Estudo

Este projeto tem como objetivo o desenvolvimento de uma API REST para gerenciamento de reservas de salas de estudo.

O sistema deve seguir arquitetura em camadas e respeitar regras de negócio relacionadas a cadastro, reservas, conflitos de horário e cancelamento.

A atividade foi planejada para você desenvolver aproximadamente 50% do código.

---

## Objetivo

Construir uma API capaz de:

- cadastrar usuários
- cadastrar salas
- realizar reservas
- listar reservas
- cancelar reservas
- validar conflitos de horário
- aplicar regras de limite por usuário

---

## Contexto

Uma instituição precisa organizar o uso de salas de estudo em grupo.

Cada usuário pode reservar salas por faixa de horário, mas o sistema deve impedir conflitos e controlar limites de uso.

---

## Estrutura do Projeto

A aplicação deve seguir a seguinte organização:

```text
salas_api/
├── domain/
├── schemas/
├── repositories/
├── services/
├── api/routes/
└── main.py
````

---

## Entidades do Sistema

### Usuario

Representa a pessoa que faz a reserva.

Campos esperados:

* `id`
* `nome`
* `email`

---

### Sala

Representa uma sala disponível para reserva.

Campos esperados:

* `id`
* `nome`
* `capacidade`
* `bloco`

---

### Reserva

Representa uma reserva realizada por um usuário para uma sala.

Campos esperados:

* `id`
* `usuario_id`
* `sala_id`
* `data`
* `hora_inicio`
* `hora_fim`
* `status`

---

## Status possíveis da reserva

A reserva pode assumir os seguintes estados:

* `active`
* `canceled`
* `finished`

---

## Regras de Negócio

### 1. Cadastro de usuário

* não permitir email duplicado
* nome e email são obrigatórios

---

### 2. Cadastro de sala

* capacidade deve ser maior que zero
* nome da sala deve ser obrigatório

---

### 3. Criação da reserva

* não pode reservar sala para horário passado
* hora final deve ser maior que hora inicial
* a mesma sala não pode ter reservas com sobreposição de horário na mesma data
* o mesmo usuário não pode ter duas reservas com sobreposição de horário na mesma data
* um usuário pode ter no máximo 2 reservas ativas por dia
* a duração máxima de uma reserva é de 2 horas

---

### 4. Cancelamento

* apenas reservas com status `active` podem ser canceladas
* reservas já canceladas não podem ser canceladas novamente
* reservas finalizadas não podem ser canceladas

---

### 5. Finalização

* apenas reservas ativas podem ser finalizadas
* uma reserva só pode ser finalizada após o horário de término

---

## O que o aluno deve desenvolver

O aluno deve completar:

* validações de negócio
* implementações nos services
* integração entre rota e service
* regras de conflito de horário
* regras de transição de status
* respostas esperadas da API

---

## Código parcialmente entregue

## domain/usuario.py

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Usuario:
    id: int
    nome: str
    email: str
```

---

## domain/sala.py

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Sala:
    id: int
    nome: str
    capacidade: int
    bloco: str
```

---

## domain/reserva.py

```python
class Reserva:
    def __init__(
        self,
        id: int,
        usuario_id: int,
        sala_id: int,
        data: str,
        hora_inicio: str,
        hora_fim: str,
        status: str = "active"
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.sala_id = sala_id
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.status = status

    def cancelar(self):
        pass

    def finalizar(self, hora_atual: str):
        pass

    def duracao_em_horas(self) -> float:
        pass

    def conflita_com(self, outra_reserva) -> bool:
        pass
```

### O aluno deve implementar em `Reserva`:

* cancelamento
* finalização
* cálculo de duração
* verificação de conflito entre horários

---

## schemas/usuario.py

```python
from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
```

---

## schemas/sala.py

```python
from pydantic import BaseModel

class SalaCreate(BaseModel):
    nome: str
    capacidade: int
    bloco: str

class SalaOut(BaseModel):
    id: int
    nome: str
    capacidade: int
    bloco: str
```

---

## schemas/reserva.py

```python
from pydantic import BaseModel

class ReservaCreate(BaseModel):
    usuario_id: int
    sala_id: int
    data: str
    hora_inicio: str
    hora_fim: str

class ReservaOut(BaseModel):
    id: int
    usuario_id: int
    sala_id: int
    data: str
    hora_inicio: str
    hora_fim: str
    status: str
```

---

## repositories/memory.py

```python
class MemoryDB:
    def __init__(self):
        self.usuarios = {}
        self.salas = {}
        self.reservas = {}
        self.next_usuario_id = 1
        self.next_sala_id = 1
        self.next_reserva_id = 1

db = MemoryDB()
```

---

## services/reserva_service.py

```python
from domain.usuario import Usuario
from domain.sala import Sala
from domain.reserva import Reserva
from repositories.memory import db


def criar_usuario(nome: str, email: str):
    pass


def listar_usuarios():
    pass


def criar_sala(nome: str, capacidade: int, bloco: str):
    pass


def listar_salas():
    pass


def criar_reserva(usuario_id: int, sala_id: int, data: str, hora_inicio: str, hora_fim: str):
    pass


def listar_reservas():
    pass


def listar_reservas_usuario(usuario_id: int):
    pass


def buscar_reserva(reserva_id: int):
    pass


def cancelar_reserva(reserva_id: int):
    pass


def finalizar_reserva(reserva_id: int, hora_atual: str):
    pass
```

### Você deve implementar no service:

* validação de email duplicado
* validação de capacidade da sala
* verificação se usuário existe
* verificação se sala existe
* verificação de conflito de horário
* limite de reservas por dia
* duração máxima da reserva
* mudança de status

---

## api/routes/usuarios.py

```python
from fastapi import APIRouter
from schemas.usuario import UsuarioCreate

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("")
def criar_usuario_route(data: UsuarioCreate):
    pass


@router.get("")
def listar_usuarios_route():
    pass
```

---

## api/routes/salas.py

```python
from fastapi import APIRouter
from schemas.sala import SalaCreate

router = APIRouter(prefix="/salas", tags=["Salas"])


@router.post("")
def criar_sala_route(data: SalaCreate):
    pass


@router.get("")
def listar_salas_route():
    pass
```

---

## api/routes/reservas.py

```python
from fastapi import APIRouter
from schemas.reserva import ReservaCreate

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post("")
def criar_reserva_route(data: ReservaCreate):
    pass


@router.get("")
def listar_reservas_route():
    pass


@router.get("/usuario/{usuario_id}")
def listar_reservas_usuario_route(usuario_id: int):
    pass


@router.get("/{reserva_id}")
def buscar_reserva_route(reserva_id: int):
    pass


@router.put("/{reserva_id}/cancelar")
def cancelar_reserva_route(reserva_id: int):
    pass


@router.put("/{reserva_id}/finalizar")
def finalizar_reserva_route(reserva_id: int, hora_atual: str):
    pass
```

---

## main.py

```python
from fastapi import FastAPI
from api.routes.usuarios import router as usuarios_router
from api.routes.salas import router as salas_router
from api.routes.reservas import router as reservas_router

app = FastAPI(title="API de Reserva de Salas de Estudo")

app.include_router(usuarios_router)
app.include_router(salas_router)
app.include_router(reservas_router)


@app.get("/")
def home():
    return {"message": "API online"}
```

---

## Endpoints esperados

```text
POST   /usuarios
GET    /usuarios

POST   /salas
GET    /salas

POST   /reservas
GET    /reservas
GET    /reservas/{reserva_id}
GET    /reservas/usuario/{usuario_id}

PUT    /reservas/{reserva_id}/cancelar
PUT    /reservas/{reserva_id}/finalizar
```

---

## Exemplos de payload

### Criar usuário

```json
{
  "nome": "Ana Souza",
  "email": "ana@email.com"
}
```

---

### Criar sala

```json
{
  "nome": "Sala 101",
  "capacidade": 6,
  "bloco": "A"
}
```

---

### Criar reserva

```json
{
  "usuario_id": 1,
  "sala_id": 1,
  "data": "2026-04-20",
  "hora_inicio": "14:00",
  "hora_fim": "15:30"
}
```

---

## Fluxo esperado da aplicação

1. a rota recebe a requisição
2. a rota chama o service
3. o service valida regras
4. o domínio executa comportamentos
5. o repository armazena os dados
6. a resposta retorna ao cliente

---

## Testes obrigatórios

Você deve testar, no mínimo:

* criar usuário com email válido
* impedir usuário com email duplicado
* criar sala com capacidade válida
* impedir sala com capacidade zero ou negativa
* criar reserva válida
* impedir reserva em horário passado
* impedir conflito de horário da mesma sala
* impedir conflito de horário do mesmo usuário
* impedir terceira reserva ativa no mesmo dia
* impedir reserva com mais de 2 horas
* cancelar reserva ativa
* impedir cancelar reserva já cancelada
* finalizar reserva após horário de término
* impedir finalizar antes do fim

---

## Critérios de avaliação

A atividade deve ser avaliada considerando:

* organização em camadas
* clareza do código
* implementação correta das regras
* uso adequado de classes de domínio
* integração correta entre rota, service e repository
* funcionamento dos endpoints

---

## Perguntas para reflexão

* por que conflito de horário não deve ser validado na rota?
* por que a entidade `Reserva` deve conhecer suas próprias regras?
* qual a responsabilidade do service nesse projeto?
* como essa estrutura ajuda a migrar depois para banco de dados real?

---

## Desafio opcional

* filtro de reservas por data
* listagem de salas disponíveis em um horário
* bloqueio de reserva para manutenção de sala
* endpoint de resumo por usuário

```

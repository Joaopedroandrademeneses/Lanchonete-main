````markdown
# Atividade: Evolução da API Lanchonete

## Tema

Implementar duas novas funcionalidades na API:

1. Cancelar pedido
2. Listar pedidos cancelados

A atividade deve seguir o padrão do projeto, separando responsabilidades entre:

```text
domain/
services/
api/routes/
schemas/
tests/
````
---

# Regras de Negócio

## Cancelamento de Pedido

Um pedido só pode ser cancelado se:

* O pedido existir.
* O pedido ainda não estiver finalizado.
* O pedido ainda não estiver cancelado.

Um pedido finalizado não pode ser cancelado.

Um pedido já cancelado não deve ser cancelado novamente.

---

# Endpoints que devem ser implementados

## 1. Cancelar Pedido

```http
PATCH /lanchonete/pedidos/{cod_pedido}/cancelar
```

### Resposta de sucesso

```json
{
  "ok": true,
  "mensagem": "Pedido cancelado com sucesso"
}
```

### Resposta de erro

```json
{
  "detail": "Pedido não encontrado ou não pode ser cancelado"
}
```

Status esperado:

```text
400
```

---

## 2. Listar Pedidos Cancelados

```http
GET /lanchonete/pedidos/cancelados
```

### Resposta esperada

```json
[
  {
    "codigo": 1,
    "cpf": "12345678900",
    "esta_entregue": false,
    "esta_cancelado": true,
    "produtos": [1, 2]
  }
]
```

---

# Parte 1: Domínio

Arquivo:

```text
domain/pedido.py
```

Adicionar o atributo:

```python
esta_cancelado: bool
```

No construtor da classe `Pedido`, inicializar com:

```python
self.esta_cancelado = False
```

Criar o método:

```python
def cancelar(self) -> bool:
    if self.esta_entregue:
        return False

    if self.esta_cancelado:
        return False

    # TODO: marcar o pedido como cancelado

    return True
```

---

# Parte 2: Schema

Arquivo:

```text
schemas/pedido.py
```

Atualizar o schema de saída:

```python
from pydantic import BaseModel


class PedidoOut(BaseModel):
    codigo: int
    cpf: str
    esta_entregue: bool
    esta_cancelado: bool
    produtos: list[int]
```

---

# Parte 3: Service

Arquivo:

```text
services/lanchonete_service.py
```

Adicionar os métodos:

```python
def cancelar_pedido(self, cod_pedido: int) -> bool:
    pedido = self.pedido_repository.buscar_por_codigo(cod_pedido)

    if pedido is None:
        return False

    # TODO: chamar o método cancelar do pedido

    return False
```

```python
def listar_pedidos_cancelados(self):
    pedidos = self.pedido_repository.listar_todos()

    # TODO: retornar apenas os pedidos cancelados

    return []
```

---

# Parte 4: API com 50% do código

Arquivo:

```text
api/routes/pedidos.py
```

## Endpoint 1: Cancelar pedido

```python
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/{cod_pedido}/cancelar")
def cancelar_pedido(cod_pedido: int):
    resultado = service.cancelar_pedido(cod_pedido)

    if not resultado:
        raise HTTPException(
            status_code=400,
            detail="Pedido não encontrado ou não pode ser cancelado"
        )

    return {
        "ok": True,
        "mensagem": "Pedido cancelado com sucesso"
    }
```

---

## Endpoint 2: Listar pedidos cancelados

```python
@router.get("/cancelados", response_model=list[PedidoOut])
def listar_pedidos_cancelados():
    pedidos = service.listar_pedidos_cancelados()

    resposta = []

    for pedido in pedidos:
        # TODO: montar o PedidoOut corretamente
        resposta.append(
            PedidoOut(
                codigo=pedido.codigo,
                cpf=pedido.cliente.cpf,
                esta_entregue=pedido.esta_entregue,
                esta_cancelado=pedido.esta_cancelado,
                produtos=[]  # TODO: retornar os códigos dos produtos
            )
        )

    return resposta
```

---

# Parte 5: Pytest com 25% do código

Arquivo:

```text
tests/test_api_cancelar_pedido.py
```

## Teste 1: Deve cancelar pedido com sucesso

```python
def test_deve_cancelar_pedido_com_sucesso(client):
    # TODO: criar cliente

    # TODO: criar produto

    # TODO: criar pedido

    response = client.post("/lanchonete/pedidos/1/cancelar")

    assert response.status_code == 200

    data = response.json()

    # TODO: validar se data["ok"] é True

    # TODO: validar mensagem de sucesso
```

---

## Teste 2: Não deve cancelar pedido inexistente

```python
def test_nao_deve_cancelar_pedido_inexistente(client):
    response = client.post("/lanchonete/pedidos/999/cancelar")

    # TODO: validar status_code

    data = response.json()

    # TODO: validar mensagem de erro
```

---

## Teste 3: Não deve cancelar pedido finalizado

```python
def test_nao_deve_cancelar_pedido_finalizado(client):
    # TODO: criar cliente

    # TODO: criar produto

    # TODO: criar pedido

    # TODO: finalizar pedido

    response = client.post("/lanchonete/pedidos/1/cancelar")

    # TODO: validar erro
```

---

## Teste 4: Deve listar pedidos cancelados

```python
def test_deve_listar_pedidos_cancelados(client):
    # TODO: criar cliente

    # TODO: criar produto

    # TODO: criar pedido

    # TODO: cancelar pedido

    response = client.get("/lanchonete/pedidos/cancelados")

    assert response.status_code == 200

    data = response.json()

    # TODO: validar se retornou uma lista

    # TODO: validar se existe pelo menos um pedido cancelado

    # TODO: validar se esta_cancelado é True
```

---

# Comando para executar os testes

```bash
pytest -q
```
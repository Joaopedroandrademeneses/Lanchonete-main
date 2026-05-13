````markdown
# Atividade: Evolução API Lanchonete

---

# Objetivo

O aluno deverá implementar:

1. Um campo de observação no pedido
2. Endpoint para adicionar observação
3. Endpoint para consultar observação do pedido
4. Regras de negócio no domínio e service
5. Testes automatizados com Pytest

---

# Contexto

Na lanchonete, clientes frequentemente fazem observações como:

- Sem cebola
- Carne ao ponto
- Tirar ketchup
- Adicionar molho extra
- Entregar na mesa externa

Agora o sistema deverá permitir registrar observações nos pedidos.

---

# Regras de Negócio

## Observação do Pedido

- O pedido pode possuir apenas uma observação textual.
- A observação deve ter no máximo 200 caracteres.
- Não permitir observação vazia.
- Não permitir adicionar observação em pedido finalizado.
- Se já existir observação, ela deve ser substituída pela nova.

---

# Endpoints da Atividade

## 1. Adicionar observação

```http
POST /lanchonete/pedidos/{cod_pedido}/observacao
````

### Payload esperado

```json
{
  "observacao": "Sem cebola e sem molho"
}
```

---

### Resposta de sucesso

```json
{
  "ok": true,
  "mensagem": "Observação adicionada com sucesso"
}
```

---

### Resposta de erro

```json
{
  "detail": "Pedido não encontrado ou inválido"
}
```

---

# 2. Consultar observação do pedido

```http
GET /lanchonete/pedidos/{cod_pedido}/observacao
```

---

### Resposta esperada

```json
{
  "codigo": 1,
  "observacao": "Sem cebola e sem molho"
}
```

---

# Parte 1: Domain

Arquivo:

```text
domain/pedido.py
```

---

## Adicionar atributo

```python
self.observacao = ""
```

---

## Criar método

```python
def adicionar_observacao(self, observacao: str) -> bool:
    if self.esta_entregue:
        return False

    if observacao is None:
        return False

    observacao = observacao.strip()

    if observacao == "":
        return False

    if len(observacao) > 200:
        return False

    # TODO: salvar observação

    return True
```

---

# Parte 2: Schema

Arquivo:

```text
schemas/pedido.py
```

---

## Schema de entrada

```python
from pydantic import BaseModel


class ObservacaoInput(BaseModel):
    observacao: str
```

---

## Schema de saída

```python
class ObservacaoOut(BaseModel):
    codigo: int
    observacao: str
```

---

# Parte 3: Service

Arquivo:

```text
services/lanchonete_service.py
```

---

## Método 1

```python
def adicionar_observacao(
    self,
    cod_pedido: int,
    observacao: str
) -> bool:

    pedido = self.pedido_repository.buscar_por_codigo(
        cod_pedido
    )

    if pedido is None:
        return False

    # TODO: chamar método do domínio

    return False
```

---

## Método 2

```python
def buscar_observacao_pedido(
    self,
    cod_pedido: int
):
    pedido = self.pedido_repository.buscar_por_codigo(
        cod_pedido
    )

    if pedido is None:
        return None

    return pedido
```

---

# Parte 4: API com 50% do código

Arquivo:

```text
api/routes/pedidos.py
```

---

# Endpoint 1 — Adicionar observação

```python
@router.post("/{cod_pedido}/observacao")
def adicionar_observacao(
    cod_pedido: int,
    body: ObservacaoInput
):
    resultado = service.adicionar_observacao(
        cod_pedido,
        body.observacao
    )

    if not resultado:
        raise HTTPException(
            status_code=400,
            detail="Pedido não encontrado ou inválido"
        )

    return {
        "ok": True,
        "mensagem": "Observação adicionada com sucesso"
    }
```

---

# Endpoint 2 — Buscar observação

```python
@router.get(
    "/{cod_pedido}/observacao",
    response_model=ObservacaoOut
)
def buscar_observacao(cod_pedido: int):
    pedido = service.buscar_observacao_pedido(
        cod_pedido
    )

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    return ObservacaoOut(
        codigo=pedido.codigo,
        observacao=""  # TODO
    )
```

---

# Parte 5: Pytest com 25% do código

Arquivo:

```text
tests/test_api_observacao_pedido.py
```

---

# Teste 1 — Deve adicionar observação

```python
def test_deve_adicionar_observacao(client):
    # TODO: criar cliente

    # TODO: criar produto

    # TODO: criar pedido

    response = client.post(
        "/lanchonete/pedidos/1/observacao",
        json={
            "observacao": "Sem cebola"
        }
    )

    assert response.status_code == 200

    data = response.json()

    # TODO: validar retorno
```

---

# Teste 2 — Não deve aceitar observação vazia

```python
def test_nao_deve_aceitar_observacao_vazia(client):
    response = client.post(
        "/lanchonete/pedidos/1/observacao",
        json={
            "observacao": ""
        }
    )

    # TODO: validar erro
```

---

# Teste 3 — Não deve adicionar observação em pedido finalizado

```python
def test_nao_deve_adicionar_observacao_em_pedido_finalizado(client):
    # TODO: criar cliente

    # TODO: criar produto

    # TODO: criar pedido

    # TODO: finalizar pedido

    response = client.post(
        "/lanchonete/pedidos/1/observacao",
        json={
            "observacao": "Sem molho"
        }
    )

    # TODO: validar erro
```

---

# Teste 4 — Deve buscar observação do pedido

```python
def test_deve_buscar_observacao_pedido(client):
    # TODO: criar cliente

    # TODO: criar produto

    # TODO: criar pedido

    # TODO: adicionar observação

    response = client.get(
        "/lanchonete/pedidos/1/observacao"
    )

    assert response.status_code == 200

    data = response.json()

    # TODO: validar observação
```
---

# Comando para executar os testes

```bash
pytest -q
```
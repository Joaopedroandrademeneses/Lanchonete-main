# Aula: Testes Automatizados com pytest

## O que são testes automatizados?

Testar manualmente significa abrir o Postman, preencher um formulário ou rodar o sistema e verificar com os próprios olhos se o resultado está correto. Funciona, mas tem um problema: a cada nova funcionalidade adicionada, você precisa repetir todos os testes anteriores para garantir que nada quebrou.

**Testes automatizados** são programas que fazem isso por você. Você escreve o teste uma vez e roda com um único comando. O pytest é o framework mais popular do ecossistema Python para isso.

---

## Por que testar?

- Garante que o código faz o que deveria fazer
- Detecta regressões: quando uma mudança quebra algo que funcionava antes
- Serve como documentação viva do comportamento esperado
- Dá confiança para refatorar e evoluir o código

---

## Instalação

```bash
pip install pytest httpx
```

> O `httpx` é necessário porque o `TestClient` do FastAPI o usa internamente para simular requisições HTTP.

---

## Como rodar os testes

Na raiz do projeto:

```bash
pytest -q
```

O `-q` (quiet) exibe uma saída resumida. Para ver mais detalhes:

```bash
pytest -v
```

Para rodar apenas um arquivo:

```bash
pytest tests/test_domain_produto.py -v
```

Para rodar apenas uma função:

```bash
pytest tests/test_domain_produto.py::test_produto_tipo_1_aplica_desconto -v
```

---

## Configuração: pytest.ini

O arquivo `pytest.ini` na raiz do projeto informa ao pytest onde encontrar os módulos do projeto:

```ini
[pytest]
pythonpath = .
```

Sem isso, ao importar `from main import app`, o pytest não saberia onde procurar o arquivo `main.py`.

---

## Estrutura de um teste

Todo teste no pytest é uma **função que começa com `test_`**. Dentro dela, usamos `assert` para verificar se o resultado é o esperado:

```python
def test_produto_tipo_1_aplica_desconto():
    p = Produto(codigo=1, valor=10, tipo=1, desconto_percentual=10)
    assert p.preco_final() == 9.0
```

Se o `assert` for verdadeiro → teste **passa** ✅  
Se o `assert` for falso → teste **falha** ❌ e o pytest mostra exatamente o que estava errado.

### Padrão AAA (Arrange, Act, Assert)

Uma boa prática é organizar o corpo do teste em três etapas:

```
Arrange  →  prepara os dados necessários
Act      →  executa a ação que está sendo testada
Assert   →  verifica se o resultado é o esperado
```

Exemplo aplicado:

```python
def test_produto_tipo_1_aplica_desconto():
    # Arrange
    p = Produto(codigo=1, valor=10, tipo=1, desconto_percentual=10)

    # Act
    resultado = p.preco_final()

    # Assert
    assert resultado == 9.0
```

---

## Tipos de teste

### 1. Teste unitário

Testa **uma única unidade de código** isolada, sem banco de dados, API ou componente externo. É o mais rápido e simples de escrever.

**Exemplo — `tests/test_domain_produto.py`:**

```python
from domain.produto import Produto

def test_produto_tipo_2_nao_aplica_desconto():
    p = Produto(codigo=2, valor=20, tipo=2, desconto_percentual=10)
    assert p.preco_final() == 20.0
```

Aqui testamos diretamente a regra de negócio: produto do tipo 2 nunca recebe desconto, independente do percentual informado.

---

### 2. Teste de integração

Testa **múltiplos componentes trabalhando juntos**: a rota recebe a requisição, passa pelo service, acessa o repositório e devolve a resposta. Mais lento que unitário, mas mais abrangente.

**Exemplo — `tests/test_api_clientes.py`:**

```python
def test_post_e_get_cliente(client):
    r = client.post("/clientes", json={"cpf": "11122233344", "nome": "Cliente X"})
    assert r.status_code == 200
    assert r.json()["cpf"] == "11122233344"

    r2 = client.get("/clientes/11122233344")
    assert r2.status_code == 200
    assert r2.json()["nome"] == "Cliente X"
```

---

### 3. Teste de ponta a ponta (end-to-end)

Simula **um fluxo completo de uso**, do início ao fim. No nosso projeto, isso significa criar cliente, criar produtos, abrir pedido, adicionar itens e finalizar — tudo via API.

**Exemplo — `tests/test_api_pedidos.py`:**

```python
def test_fluxo_completo_pedido(client):
    client.post("/clientes", json={"cpf": "11122233344", "nome": "Cliente X"})
    client.post("/produtos", json={"codigo": 1, "valor": 10, "tipo": 1, "desconto_percentual": 10})
    client.post("/produtos", json={"codigo": 2, "valor": 20, "tipo": 2, "desconto_percentual": 10})

    r = client.post("/lanchonete/pedidos", json={"cpf": "11122233344", "cod_produto": 1, "qtd_max_produtos": 10})
    cod_pedido = r.json()["codigo"]

    client.put(f"/lanchonete/pedidos/{cod_pedido}/itens", json={"cod_produto": 2})

    r3 = client.post(f"/lanchonete/pedidos/{cod_pedido}/finalizar")
    assert r3.json()["total"] == 29.0
```

---

### Happy path vs. Sad path

| Tipo | Descrição | Exemplo |
|---|---|---|
| **Happy path** | Fluxo normal e esperado, tudo certo | Criar cliente com CPF válido |
| **Sad path** | Entrada inválida ou situação de erro | Buscar CPF inexistente → 404 |

Sempre teste os dois! O sad path é onde muitos bugs se escondem.

```python
# sad path: cliente inexistente deve retornar 404
def test_get_cliente_inexistente(client):
    r = client.get("/clientes/000")
    assert r.status_code == 404
```

---

## Fixtures

**Fixture** é uma função reutilizável que prepara o ambiente antes do teste. O pytest a injeta automaticamente em qualquer função de teste que a declare como parâmetro.

Todas as fixtures ficam no arquivo `tests/conftest.py`, que o pytest carrega automaticamente.

### Fixture simples: `client`

```python
@pytest.fixture
def client():
    return TestClient(app)
```

**Como usar em um teste:**

```python
def test_exemplo(client):          # pytest injeta o client aqui
    r = client.get("/health")
    assert r.status_code == 200
```

O `TestClient` simula requisições HTTP diretamente na aplicação FastAPI, sem precisar de uma porta de rede. Isso torna os testes rápidos e independentes de infraestrutura.

---

### Fixture com autouse: `reset_memory_db`

```python
@pytest.fixture(autouse=True)
def reset_memory_db():
    db.clientes_por_cpf.clear()
    db.produtos_por_id.clear()
    db.pedidos_por_codigo.clear()
    yield
```

O `autouse=True` faz o pytest executar esse fixture **automaticamente antes de cada teste**, sem que o teste precise declará-lo como parâmetro.

**Por que limpar o banco antes de cada teste?**

Testes não podem depender uns dos outros. Se um teste criar um cliente e o próximo esperar que o banco esteja vazio, o segundo falhará por causa do estado deixado pelo primeiro. O isolamento garante que cada teste é independente.

---

### O papel do `yield` nas fixtures

O `yield` divide a fixture em duas fases:

```
tudo antes do yield  →  fase de PREPARAÇÃO (setup)
tudo depois do yield →  fase de LIMPEZA    (teardown)
```

**Exemplo com limpeza após o teste:**

```python
@pytest.fixture
def arquivo_temporario():
    caminho = "/tmp/teste.txt"
    open(caminho, "w").close()   # prepara
    yield caminho                # devolve para o teste usar
    os.remove(caminho)           # limpa depois que o teste terminar
```

No nosso caso, a limpeza é feita **antes** (no início do fixture), mas o `yield` ainda é necessário para o pytest saber quando o teste executou.

---

## Isolamento de testes

Um princípio fundamental: **cada teste deve ser independente**.

❌ **Errado** — segundo teste depende do primeiro:
```python
def test_1_cria_cliente(client):
    client.post("/clientes", json={"cpf": "111", "nome": "X"})

def test_2_busca_cliente(client):
    r = client.get("/clientes/111")   # falha se test_1 não rodou antes!
    assert r.status_code == 200
```

✅ **Certo** — cada teste cria o que precisa:
```python
def test_busca_cliente(client):
    client.post("/clientes", json={"cpf": "111", "nome": "X"})  # prepara
    r = client.get("/clientes/111")
    assert r.status_code == 200
```

---

## Mapa dos testes do projeto

```
tests/
│
├── conftest.py              # fixtures compartilhadas (client, reset_memory_db)
│
├── test_domain_produto.py   # unitários — regras de desconto de Produto
│   ├── test_produto_tipo_1_aplica_desconto
│   ├── test_produto_tipo_2_nao_aplica_desconto
│   └── test_produto_sem_desconto
│
├── test_domain_pedido.py    # unitários — regras de negócio de Pedido
│   ├── test_pedido_limite_itens
│   ├── test_pedido_total_se_nao_finalizado_retorna_0
│   └── test_pedido_finalizar_calcula_total_com_regras
│
├── test_api_clientes.py     # integração — endpoints de clientes
│   ├── test_post_e_get_cliente        (happy path)
│   └── test_get_cliente_inexistente   (sad path)
│
└── test_api_pedidos.py      # end-to-end — ciclo completo de um pedido
    └── test_fluxo_completo_pedido
```

---

## Pirâmide de testes

```
        /\
       /E2E\         poucos, lentos, abrangentes
      /------\
     / Integr.\      médios em quantidade e velocidade
    /----------\
   /  Unitários \    muitos, rápidos, isolados
  /--------------\
```

A base da pirâmide deve ter muitos testes unitários (rápidos e baratos). O topo deve ter poucos testes end-to-end (lentos e caros de manter). Não inverta a pirâmide.

---

## Atividade prática

Com base no projeto da lanchonete, escreva os seguintes testes:

1. **Unitário**: Produto com valor negativo deve lançar `ValueError`
2. **Unitário**: Pedido com `qtd_max_produtos=0` deve lançar `ValueError`
3. **Integração**: `POST /clientes` com CPF vazio deve retornar status `400`
4. **Integração**: `PUT /produtos/{codigo}/valor` deve atualizar o valor e retornar `{"alterou": true}`
5. **End-to-end**: Criar um pedido e buscá-lo pelo código via `GET /lanchonete/pedidos/{cod_pedido}`

> **Dica:** Para testar se uma exceção é lançada, use `pytest.raises`:
> ```python
> import pytest
> from domain.produto import Produto
>
> def test_produto_valor_negativo():
>     with pytest.raises(ValueError):
>         Produto(codigo=1, valor=-5, tipo=1)
> ```

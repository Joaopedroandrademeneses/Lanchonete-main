# =============================================================================
# test_api_atividades.py — Atividades práticas da Aula 08: ORM Tortoise
# =============================================================================
#
# Este arquivo contém os 5 testes pedidos na atividade prática do arquivo:
#   atividades/Treino Apis/8 - Aula ORM Tortoise.md
#
# Todos os testes de API são async porque:
#   - O Tortoise ORM exige await em qualquer operação de banco
#   - O AsyncClient (httpx) também é assíncrono
#   - O pytest-asyncio (asyncio_mode = auto no pytest.ini) detecta
#     automaticamente funções async def test_* e as executa corretamente
#
# O fixture `client` e o `init_test_db` (autouse) estão definidos em
# conftest.py e são injetados automaticamente pelo pytest em cada teste.
# Não é necessário importá-los aqui.
# =============================================================================


# -----------------------------------------------------------------------------
# HELPERS — dados reutilizados entre os testes
# -----------------------------------------------------------------------------

CLIENTE_PADRAO = {"cpf": "11122233344", "nome": "Cliente Teste"}
PRODUTO_COM_DESCONTO = {"codigo": 1, "valor": 10.0, "tipo": 1, "desconto_percentual": 10.0}
PRODUTO_SEM_DESCONTO = {"codigo": 2, "valor": 20.0, "tipo": 2, "desconto_percentual": 0.0}


# -----------------------------------------------------------------------------
# ATIVIDADE 1 — Integração: Produto não encontrado deve retornar 404
# -----------------------------------------------------------------------------

async def test_get_produto_inexistente(client):
    """Buscar um produto com código que não existe deve retornar 404.

    Este é um teste de caminho negativo (sad path): verifica que a API
    responde corretamente quando o recurso solicitado não está no banco.

    Fluxo:
        - Nenhum produto é criado (banco vazio pelo init_test_db)
        - GET /produtos/9999 → produto com código 9999 não existe
        - Esperado: status 404
    """
    response = await client.get("/produtos/9999")

    assert response.status_code == 404


# -----------------------------------------------------------------------------
# ATIVIDADE 2 — Integração: Criar produto e atualizar seu valor
# -----------------------------------------------------------------------------

async def test_atualizar_valor_produto(client):
    """Deve ser possível criar um produto e alterar seu valor via PUT.

    Fluxo:
        1. POST /produtos        → cria o produto com valor 50.0
        2. PUT /produtos/{cod}/valor → altera para 99.0
        3. Verificações:
            - Status da alteração é 200
            - Body retornado contém {"alterou": true}

    Por que verificar o body?
        A rota retorna um dicionário explícito confirmando a operação.
        Isso garante que o serviço processou a mudança (e não só aceitou
        a requisição sem fazer nada).
    """
    # 1. Cria o produto
    r_criar = await client.post("/produtos", json={
        "codigo": 10, "valor": 50.0, "tipo": 1, "desconto_percentual": 5.0
    })
    assert r_criar.status_code == 200

    # 2. Altera o valor do produto criado
    r_alterar = await client.put("/produtos/10/valor", json={"novo_valor": 99.0})

    # 3. Verifica resposta
    assert r_alterar.status_code == 200
    assert r_alterar.json() == {"alterou": True}


# -----------------------------------------------------------------------------
# ATIVIDADE 3 — End-to-end: Buscar pedido pelo código após criação
# -----------------------------------------------------------------------------

async def test_buscar_pedido_por_codigo(client):
    """Deve ser possível buscar um pedido pelo código retornado na criação.

    Estende o fluxo do test_fluxo_completo_pedido adicionando a etapa
    de busca do pedido via GET após sua criação.

    Fluxo:
        1. Cria cliente e produto (pré-requisitos do pedido)
        2. POST /lanchonete/pedidos  → cria o pedido, salva o código
        3. GET /lanchonete/pedidos/{cod_pedido} → busca pelo código
        4. Verificações:
            - Status da busca é 200
            - O CPF retornado bate com o do cliente que fez o pedido

    Por que salvar cod_pedido?
        O código é gerado automaticamente pelo banco (autoincrement).
        Precisamos do valor retornado na criação para referenciar
        o pedido nas chamadas seguintes.
    """
    # 1. Pré-requisitos: cliente e produto devem existir antes do pedido
    await client.post("/clientes", json=CLIENTE_PADRAO)
    await client.post("/produtos", json=PRODUTO_COM_DESCONTO)

    # 2. Cria o pedido e extrai o código gerado pelo banco
    r_criar = await client.post("/lanchonete/pedidos", json={
        "cpf": CLIENTE_PADRAO["cpf"],
        "cod_produto": PRODUTO_COM_DESCONTO["codigo"],
        "qtd_max_produtos": 5,
    })
    assert r_criar.status_code == 200
    cod_pedido = r_criar.json()["codigo"]

    # 3. Busca o pedido pelo código
    r_buscar = await client.get(f"/lanchonete/pedidos/{cod_pedido}")

    # 4. Verificações
    assert r_buscar.status_code == 200
    assert r_buscar.json()["cpf"] == CLIENTE_PADRAO["cpf"]


# -----------------------------------------------------------------------------
# ATIVIDADE 4 — Integração: CPF vazio deve ser rejeitado com 400
# -----------------------------------------------------------------------------

async def test_criar_cliente_cpf_vazio(client):
    """Tentar criar um cliente com CPF vazio deve retornar 400.

    O serviço (lanchonete_service.py) valida que o CPF não pode ser
    vazio ou conter apenas espaços. Quando essa regra é violada, ele
    lança ValueError, que a rota converte em HTTPException 400.

    Fluxo:
        - POST /clientes com cpf="" (string vazia)
        - Esperado: status 400

    Este teste garante que a validação de negócio está conectada
    corretamente à camada HTTP (a rota captura o ValueError do serviço).
    """
    response = await client.post("/clientes", json={"cpf": "", "nome": "X"})

    assert response.status_code == 400


# -----------------------------------------------------------------------------
# ATIVIDADE 5 — Sad path: Adicionar produto além do limite deve retornar 400
# -----------------------------------------------------------------------------

async def test_pedido_com_limite_atingido(client):
    """Tentar adicionar produto além do limite do pedido deve retornar 400.

    A regra de negócio: um pedido tem qtd_max_produtos. Ao atingir o
    limite, qualquer tentativa de adicionar mais itens é rejeitada.

    Fluxo:
        1. Cria cliente e dois produtos
        2. Cria pedido com qtd_max_produtos=1 (já inclui o produto 1)
           → pedido começa com 1 item, que é o máximo
        3. Tenta adicionar o produto 2 via PUT /itens
           → limite já atingido, deve retornar 400

    Por que qtd_max_produtos=1?
        A criação do pedido já inclui o primeiro produto automaticamente.
        Com limite 1, qualquer adição extra já viola a regra.
    """
    # 1. Pré-requisitos
    await client.post("/clientes", json={"cpf": "99988877766", "nome": "Ana"})
    await client.post("/produtos", json={
        "codigo": 5, "valor": 10.0, "tipo": 2, "desconto_percentual": 0.0
    })
    await client.post("/produtos", json={
        "codigo": 6, "valor": 15.0, "tipo": 2, "desconto_percentual": 0.0
    })

    # 2. Cria pedido com limite de 1 produto (produto 5 já é incluído na criação)
    r_criar = await client.post("/lanchonete/pedidos", json={
        "cpf": "99988877766",
        "cod_produto": 5,
        "qtd_max_produtos": 1,   # ← limite máximo: 1 item (já atingido)
    })
    assert r_criar.status_code == 200
    cod_pedido = r_criar.json()["codigo"]

    # 3. Tenta adicionar produto 6 — deve ser bloqueado pelo limite
    r_adicionar = await client.put(
        f"/lanchonete/pedidos/{cod_pedido}/itens",
        json={"cod_produto": 6},
    )

    assert r_adicionar.status_code == 400

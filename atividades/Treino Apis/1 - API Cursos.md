```markdown
# API de Plataforma de Cursos Online

Este projeto consiste no desenvolvimento de uma API REST utilizando arquitetura em camadas. O objetivo é estruturar corretamente uma aplicação backend, separando responsabilidades e implementando regras de negócio de forma organizada.

O código não será fornecido completo. A proposta é que a API seja construída a partir das definições e assinaturas apresentadas neste documento.

---

## Objetivo

Desenvolver uma API que permita:

- Cadastro de alunos
- Cadastro de cursos
- Consulta de dados
- Aplicação de regras de preço

O foco principal é compreender como estruturar uma aplicação backend de forma adequada.

---

## Contexto

Uma empresa deseja criar uma plataforma de cursos online simples.

Os requisitos são:

- Alunos podem ser cadastrados no sistema
- Cursos podem ser gratuitos ou pagos
- Cursos pagos podem ter desconto
- As informações devem ser consultáveis via API

---

## Estrutura do Projeto

A aplicação deve seguir a seguinte organização:

```

cursos_api/
├── domain/
├── schemas/
├── repositories/
├── services/
├── api/routes/
└── main.py

````

Cada diretório possui uma responsabilidade específica:

- domain: entidades e regras de negócio
- schemas: definição de entrada e saída da API
- repositories: acesso a dados (em memória)
- services: lógica da aplicação
- api/routes: definição dos endpoints

---

## Entidades

### Aluno

Campos esperados:

- id (gerado automaticamente)
- nome
- email

### Curso

Campos esperados:

- codigo
- titulo
- preco
- tipo (1 = gratuito, 2 = pago)
- desconto_percentual (opcional)

---

## Regras de Negócio

As seguintes regras devem ser implementadas:

- Cursos do tipo 1 (gratuitos) devem ter preço final igual a 0
- Cursos do tipo 2 (pagos) podem receber desconto
- O desconto deve ser aplicado sobre o valor do curso
- O preço final nunca pode ser negativo

A regra de cálculo deve estar no domínio, não nas rotas.

---

## Assinaturas Obrigatórias

### Domain

```python
class Curso:
    def __init__(self, codigo: int, titulo: str, preco: float, tipo: int, desconto_percentual: float = 0):
        pass

    def preco_final(self) -> float:
        pass
````

---

### Services

```python
def criar_aluno(nome: str, email: str):
    pass

def listar_alunos():
    pass

def criar_curso(codigo: int, titulo: str, preco: float, tipo: int):
    pass

def listar_cursos():
    pass

def buscar_curso(codigo: int):
    pass

def atualizar_preco(codigo: int, novo_preco: float):
    pass
```

---

## Endpoints Esperados

A API deve expor os seguintes endpoints:

```
POST   /alunos
GET    /alunos

POST   /cursos
GET    /cursos
GET    /cursos/{codigo}
PUT    /cursos/{codigo}/preco
GET    /cursos/{codigo}/preco-final
```

---

## Fluxo da Aplicação

O fluxo esperado é:

1. A requisição chega na rota
2. A rota chama o service
3. O service aplica as regras de negócio
4. O repository armazena ou consulta os dados
5. A resposta é retornada ao cliente

---

## Testes

Os seguintes cenários devem ser testados:

* Criar aluno
* Listar alunos
* Criar curso
* Listar cursos
* Buscar curso por código
* Atualizar preço
* Verificar cálculo de preço final

---

## Regras de Implementação

Durante o desenvolvimento, observe:

* Não colocar regra de negócio nas rotas
* Não usar apenas dicionários como modelo principal
* Não misturar camadas (domain, service, API)
* Manter o código organizado e legível

---

## Entrega

A entrega deve conter:

* API funcional
* Estrutura de pastas conforme especificado
* Implementação correta das regras de negócio
* Endpoints funcionando via Swagger

---

## Perguntas para Reflexão

* Qual a responsabilidade da camada de domínio?
* Por que a lógica não deve ficar na rota?
* Qual o papel do service na aplicação?
* Como essa organização facilita manutenção futura?

---

## Extensão (opcional)

Implementar um endpoint adicional:

```
GET /cursos/{codigo}/detalhado
```

Retornando:

* Dados do curso
* Preço original
* Preço final calculado
* Tipo do curso formatado

---

```

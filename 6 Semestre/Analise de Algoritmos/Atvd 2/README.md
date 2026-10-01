# Banco Meridian — Exercícios de Algoritmos

Você vai completar o "core" do cadastro de clientes de um banco fictício
(Banco Meridian). A aplicação (dados, telas e testes) já está pronta; faltam
as funções e classes em `src/algoritmos/`, que hoje apenas lançam
`NotImplementedError`.

Cada exercício é uma operação real do cadastro, acessível por um botão no menu
da aplicação. Os testes em `tests/` descrevem o contrato esperado de cada uma.

## Requisitos

- Python 3.10+
- Dependências: `textual`, `pytest`, `hypothesis` (ver `requirements.txt`)

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Como executar

Da raiz do projeto:

```bash
python -m src.main clientes.csv
```

Por padrão a aplicação carrega as primeiras 100.000 linhas do arquivo. Use
`--n` para mudar o tamanho da amostra carregada (ex.: `--n 5000000` para tudo):

```bash
python -m src.main clientes.csv --n 5000000
```

Abre a aplicação. Escolha um exercício no menu e clique em **Executar**. Os
exercícios de verificação de CPF, autocomplete e busca textual têm também um
campo de texto para você testar interativamente (com o tempo gasto em cada
consulta).

## Gerar o conjunto de dados

O arquivo de dados (`clientes.csv`) não acompanha o projeto: gere-o antes de
executar. O gerador é determinístico — com a mesma semente, o resultado é
sempre idêntico.

Para gerar o conjunto completo (5.000.000 de clientes, ~455 MB):

```bash
python gerar_seed.py
```

O gerador usa a semente fixa `3`. Se quiser gerar uma quantidade menor para
testes, use o módulo diretamente (mantendo a mesma semente):

```bash
python -m src.dados.gerador 100000 --seed 3 --caminho clientes.csv
```

Cada linha tem: nome, cpf, idade, renda_anual, patrimonio_total,
dividas_totais, nascimento, email.

## O que implementar

Tudo está em `src/algoritmos/`. Não altere as assinaturas das funções e
classes — a aplicação e os testes dependem delas.

| Exercício (tela)            | Operação do cadastro                       | A implementar                              |
|-----------------------------|--------------------------------------------|--------------------------------------------|
| 1. Relatório gerencial      | listar clientes por idade                  | `ordenar_idade(colecao)`                   |
| 2. Remessas fiscais         | ordenar clientes por CPF                   | `ordenar_cpf(colecao)`                     |
| 3. Private Banking          | os 10 clientes com maior patrimônio        | `selecionar_topk(colecao, chave, k)`       |
| 4. Consulta central         | localizar um cliente por CPF               | `buscar(colecao_ordenada, chave, valor)`   |
| 5. Cache de acesso          | guardar e consultar cliente por CPF        | `Indice.put(chave, valor)` / `Indice.get(chave)` |
| 6. Verificação pré-cadastro | saber se um CPF já existe                  | `Existencia.add(item)` / `Existencia.contem(item)` |
| 7. Atendimento              | autocompletar o nome no formulário         | `Prefixo.adicionar(texto)` / `Prefixo.completar(prefixo)` |
| 8. Busca textual            | achar um trecho de texto nos nomes         | `achar_substring(texto, padrao)`           |

A docstring de cada item descreve o contrato: entradas, saída e o que a função
deve garantir. Leia-a antes de começar.

## Testes

```bash
python -m pytest tests/
```

Os testes descrevem o contrato esperado. Eles **falham** (`NotImplementedError`)
enquanto você não implementar e **passam** quando a implementação está correta.
Enquanto estiver desenvolvendo um exercício, rode apenas os testes dele:

```bash
python -m pytest tests/ -k ordenar
python -m pytest tests/ -k buscar
python -m pytest tests/ -k prefixo
```

## Regras

- Não altere as assinaturas das funções e classes em `src/algoritmos/`.
- Implemente a lógica você mesmo: não delegue o exercício inteiro a funções ou
  estruturas prontas da biblioteca padrão.
- Você pode adicionar funções auxiliares dentro do próprio arquivo do exercício.

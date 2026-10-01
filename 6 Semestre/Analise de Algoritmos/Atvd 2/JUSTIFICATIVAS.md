# Justificativa dos algoritmos — Atividade "Algoritmos com IA"

Cada função/classe que faltava em `src/algoritmos/` foi implementada escolhendo o
algoritmo adequado ao **formato do dado** e ao **uso real** de cada operação do cadastro.

| # | Operação | Algoritmo | Complexidade | Por que este |
|---|---|---|---|---|
| 1 | `ordenar_idade` | Counting sort | O(n + 121) | idade é inteiro de faixa pequena e conhecida (0–120): dá para contar ocorrências e reconstruir, sem nenhuma comparação |
| 2 | `ordenar_cpf` | Radix sort LSD | O(11 · n) | CPF é string de 11 dígitos de tamanho fixo; 11 passadas de baldes ordenam sem comparar strings |
| 3 | `selecionar_topk` | Min-heap de tamanho k | O(n log k) | Só interessam os 10 maiores: manter um heap de 10 evita ordenar os 5 milhões |
| 4 | `buscar` | Busca binária | O(log n) | A coleção já chega ordenada por CPF: divide o espaço pela metade a cada passo |
| 5 | `Indice` | Tabela hash com encadeamento | O(1) médio | Cache de acesso por CPF: é consulta direta por chave, sem ordem envolvida |
| 6 | `Existencia` | Filtro de Bloom | O(k) por consulta | Só precisa responder "já existe?" gastando pouquíssima memória; nunca dá falso negativo |
| 7 | `Prefixo` | Trie (árvore de prefixos) | O(len do prefixo + resultados) | Autocomplete: descer o prefixo uma vez e coletar apenas o ramo abaixo |
| 8 | `achar_substring` | Boyer-Moore-Horspool | O(n) típico, sublinear na prática | Compara da direita para a esquerda e usa a tabela de deslocamentos para pular blocos |

## Detalhes de implementação

- **Counting sort**: o índice do balde é a própria idade, então a lista final já sai
  ordenada e a ordem relativa de idades iguais é preservada (estável).
- **Radix sort**: como todos os CPFs têm 11 dígitos, o número de passadas é fixo.
  Dígitos iguais em todas as chaves podem ser pulados quando só o final varia.
- **Min-heap**: guarda só k itens; um novo item entra se for maior que o menor do heap.
  O empate de valores é desempatado por um contador de ordem — sem isso o Python tentaria
  comparar os objetos `Pessoa` entre si e estouraria.
- **Filtro de Bloom**: `m = -n·ln(p)/(ln2)²` bits e `k = (m/n)·ln2` funções de hash.
  Usa FNV-1a em vez do `hash()` do Python, que é randomizado a cada execução e tornaria
  o filtro inconsistente entre processos.
- **Trie**: o marcador de fim de palavra é um objeto sentinela, não o caractere `"\x00"` —
  assim um texto que contenha esse caractere não gera resultado errado.

## Como rodar

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest tests/          # 18 testes
.venv/bin/python teste_real.py             # demonstração com 200 mil clientes
```

## Resultados medidos (200.000 clientes)

| Operação | Tempo |
|---|---|
| `ordenar_idade` | 0,032 s |
| `ordenar_cpf` | 0,592 s |
| `selecionar_topk` (top 10) | 0,017 s |
| `buscar` (busca binária) | 0,032 ms por consulta |
| `Indice.get` | 0,004 ms |
| `Existencia` (Bloom) | 0 falsos negativos · 0,87% de falsos positivos |
| `Prefixo.completar("Ana")` | 0,126 ms |
| `achar_substring("silva")` | 0,193 s em 200 mil nomes |

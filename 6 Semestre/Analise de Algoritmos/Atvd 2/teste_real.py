"""Teste da aplicação real: gera dados e roda as 8 operações do enunciado."""
import time
from src.dados.gerador import main as gerar
from src.dados.modelo import carregar
from src.algoritmos import busca, existencia, indexacao, ordenacao, padroes, prefixo, selecao

print("== gerando 200k clientes (semente 3) ==")
t0 = time.perf_counter()
gerar(total=200_000, seed=3, caminho="clientes_teste.csv")
print(f"  gerado em {time.perf_counter()-t0:.2f}s")

amostra = carregar("clientes_teste.csv", limite=200_000)
print(f"  carregados: {len(amostra)}")

print("\n1) Relatório gerencial — ordenar_idade")
t0 = time.perf_counter(); r = ordenacao.ordenar_idade(amostra); dt = time.perf_counter()-t0
print(f"   {dt:.3f}s | ordenado: {[p.idade for p in r[:5]]} ... {[p.idade for p in r[-3:]]}")

print("\n2) Remessas fiscais — ordenar_cpf")
t0 = time.perf_counter(); r = ordenacao.ordenar_cpf(amostra); dt = time.perf_counter()-t0
print(f"   {dt:.3f}s | primeiros CPFs: {[p.cpf for p in r[:3]]}")

print("\n3) Private Banking — selecionar_topk(patrimonio_total, 10)")
t0 = time.perf_counter(); r = selecao.selecionar_topk(amostra, "patrimonio_total", 10); dt = time.perf_counter()-t0
print(f"   {dt:.3f}s")
for i, p in enumerate(r, 1):
    print(f"   {i:>2}. {p.nome:<30} {p.patrimonio_total:>15,}")

print("\n4) Consulta central — buscar (coleção ordenada por cpf)")
ordenada = ordenacao.ordenar_cpf(amostra)
alvo = ordenada[len(ordenada)//2].cpf
t0 = time.perf_counter(); pos = busca.buscar(ordenada, "cpf", alvo); dt = time.perf_counter()-t0
print(f"   {dt*1000:.4f}ms | pos={pos} cpf={alvo} confere={ordenada[pos].cpf == alvo}")
print(f"   ausente '00000000000' -> {busca.buscar(ordenada, 'cpf', '00000000000')}")

print("\n5) Cache de acesso — Indice")
idx = indexacao.Indice()
t0 = time.perf_counter()
for p in amostra:
    idx.put(p.cpf, p)
dt = time.perf_counter()-t0
t0 = time.perf_counter(); achado = idx.get(alvo); dt2 = time.perf_counter()-t0
print(f"   indexou {len(amostra)} em {dt:.3f}s")
print(f"   get({alvo}) -> {achado.nome if achado else None} em {dt2*1000:.4f}ms | inexistente={idx.get('00000000000')}")

print("\n6) Verificação pré-cadastro — Existencia (Bloom)")
ex = existencia.Existencia(esperados=len(amostra), falso_positivo=0.01)
t0 = time.perf_counter()
for p in amostra:
    ex.add(p.cpf)
dt = time.perf_counter()-t0
falsos_neg = sum(1 for p in amostra if not ex.contem(p.cpf))
import random
random.seed(1)
ausentes = [f"{random.randint(0, 10**11-1):011d}" for _ in range(20_000)]
falsos_pos = sum(1 for c in ausentes if ex.contem(c))
print(f"   add de {len(amostra)} em {dt:.3f}s")
print(f"   falsos negativos: {falsos_neg} (tem que ser 0)")
print(f"   falsos positivos: {falsos_pos}/{len(ausentes)} = {falsos_pos/len(ausentes)*100:.2f}% (alvo ~1%)")

print("\n7) Atendimento — Prefixo (autocomplete)")
pf = prefixo.Prefixo()
t0 = time.perf_counter()
for p in amostra:
    pf.adicionar(p.nome)
dt = time.perf_counter()-t0
t0 = time.perf_counter(); sug = pf.completar("Ana"); dt2 = time.perf_counter()-t0
print(f"   indexou {len(amostra)} nomes em {dt:.3f}s")
print(f"   completar('Ana') -> {len(sug)} sugestões em {dt2*1000:.3f}ms: {sug[:5]}")

print("\n8) Busca textual — achar_substring")
t0 = time.perf_counter()
ocor = sum(1 for p in amostra if padroes.achar_substring(p.nome.lower(), "silva"))
dt = time.perf_counter()-t0
print(f"   {ocor} nomes contêm 'silva' em {dt:.3f}s")
print(f"   sobreposição 'aaaa' em 'aaaaa' -> {padroes.achar_substring('aaaaa', 'aaaa')}")
print(f"   sem ocorrência -> {padroes.achar_substring('abc', 'zz')}")

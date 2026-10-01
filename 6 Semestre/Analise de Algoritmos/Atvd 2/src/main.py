import argparse
from pathlib import Path

from textual import work
from textual.app import App
from textual.widgets import LoadingIndicator, Static

from src.dados.modelo import carregar
from src.ui.telas import MenuScreen


def app_factory(amostra: list | None):
    class TreinadorApp(App):
        CSS = """
        #menu { padding: 1 2; }
        Button { margin: 0 0 1 0; width: 60; }
        #ex-loading { height: 1; margin: 0 0 1 0; }
        """

        def __init__(self):
            super().__init__()
            self.title = "Banco Meridian — Treinador de Algoritmos"
            self.amostra = amostra
            self._estrutura_existencia = None
            self._cpf_exemplo = None
            self._estrutura_prefixo = None
            self._amostra_texto = None

        def on_mount(self) -> None:
            self.push_screen(MenuScreen())

        def executar_exercicio(self, titulo: str) -> None:
            if self.amostra is None:
                self.screen.query_one("#ex-resultado", Static).update(
                    "Sem dados — rode com: python -m src.main <arquivo.csv> [--n N]"
                )
                return
            self.screen.query_one("#ex-loading", LoadingIndicator).display = True
            self.screen.query_one("#ex-resultado", Static).update("")
            self.rodar_exercicio(titulo)

        @work(thread=True)
        def rodar_exercicio(self, titulo: str) -> None:
            import time

            from src.algoritmos import (busca, existencia, indexacao,
                                        ordenacao, padroes, prefixo, selecao)
            t0 = time.perf_counter()
            detalhe = ""
            self._estrutura_existencia = None
            self._cpf_exemplo = None
            self._estrutura_prefixo = None
            self._amostra_texto = None
            try:
                if titulo.startswith("Relatório"):
                    ordenacao.ordenar_idade(self.amostra)
                elif titulo.startswith("Remessas"):
                    ordenacao.ordenar_cpf(self.amostra)
                elif titulo.startswith("Private"):
                    topk = selecao.selecionar_topk(self.amostra, "patrimonio_total", 10)
                    detalhe = "\n".join(
                        f"{i + 1:>2}. {p.nome} — {p.patrimonio_total:>12,}"
                        for i, p in enumerate(topk)
                    )
                elif titulo.startswith("Consulta"):
                    ordenada = sorted(self.amostra, key=lambda p: p.cpf)
                    alvo = ordenada[len(ordenada) // 2].cpf
                    busca.buscar(ordenada, "cpf", alvo)
                elif titulo.startswith("Cache"):
                    idx = indexacao.Indice()
                    for p in self.amostra:
                        idx.put(p.cpf, p)
                elif titulo.startswith("Verificação"):
                    ex = existencia.Existencia(esperados=len(self.amostra))
                    for p in self.amostra:
                        ex.add(p.cpf)
                    self._estrutura_existencia = ex
                    self._cpf_exemplo = self.amostra[0].cpf
                elif titulo.startswith("Atendimento"):
                    pf = prefixo.Prefixo()
                    for p in self.amostra:
                        pf.adicionar(p.nome)
                    self._estrutura_prefixo = pf
                elif titulo.startswith("Busca textual"):
                    self._amostra_texto = self.amostra
                    sum(
                        padroes.achar_substring(p.nome.lower(), "silva") != []
                        for p in self.amostra
                    )
                status = "OK"
            except NotImplementedError:
                status = "PENDENTE (algoritmo não implementado)"
            except Exception as err:
                status = f"ERRO: {err}"
            dt = time.perf_counter() - t0
            self.call_from_thread(
                self._concluir_exercicio, status, dt, detalhe
            )

        def _concluir_exercicio(self, status: str, dt: float, detalhe: str = "") -> None:
            self.screen.query_one("#ex-loading", LoadingIndicator).display = False
            texto = f"{status}  —  {dt:.3f}s"
            if detalhe:
                texto += f"\n\n{detalhe}"
            if self._estrutura_existencia is not None and self._cpf_exemplo is not None:
                texto += f"\n\nTeste um CPF no campo abaixo (ex.: {self._cpf_exemplo})."
            if self._estrutura_prefixo is not None:
                texto += "\n\nDigite um prefixo de nome no campo abaixo para ver sugestões."
            if self._amostra_texto is not None:
                texto += "\n\nDigite um texto no campo abaixo para buscar nos nomes."
            self.screen.query_one("#ex-resultado", Static).update(texto)

        def testar_cpf(self, cpf: str) -> None:
            import time

            estrutura = getattr(self, "_estrutura_existencia", None)
            if estrutura is None:
                self.screen.query_one("#ex-resultado", Static).update(
                    "Primeiro clique em Executar para montar a estrutura."
                )
                return
            cpf = cpf.strip()
            if not cpf:
                self.screen.query_one("#ex-resultado", Static).update(
                    "Digite um CPF."
                )
                return
            t0 = time.perf_counter()
            existe = estrutura.contem(cpf)
            dt = time.perf_counter() - t0
            resultado = "ENCONTRADO" if existe else "NÃO ENCONTRADO"
            self.screen.query_one("#ex-resultado", Static).update(
                f"CPF {cpf}: {resultado}  —  {dt:.6f}s"
            )

        def autocompletar(self, prefixo: str) -> None:
            import time

            estrutura = self._estrutura_prefixo
            if estrutura is None:
                self.screen.query_one("#ex-resultado", Static).update(
                    "Primeiro clique em Executar para montar a estrutura."
                )
                return
            prefixo = prefixo.strip()
            if not prefixo:
                self.screen.query_one("#ex-resultado", Static).update(
                    "Digite um prefixo de nome."
                )
                return
            t0 = time.perf_counter()
            sugestoes = estrutura.completar(prefixo)[:10]
            dt = time.perf_counter() - t0
            if sugestoes:
                lista = "\n".join(f"  {s}" for s in sugestoes)
                texto = f"{len(sugestoes)} sugestões  —  {dt:.6f}s\n{lista}"
            else:
                texto = f"Nenhuma sugestão  —  {dt:.6f}s"
            self.screen.query_one("#ex-resultado", Static).update(texto)

        def buscar_textual(self, texto: str) -> None:
            import time

            from src.algoritmos.padroes import achar_substring

            amostra = self._amostra_texto
            if amostra is None:
                self.screen.query_one("#ex-resultado", Static).update(
                    "Primeiro clique em Executar para carregar a base."
                )
                return
            texto = texto.strip().lower()
            if not texto:
                self.screen.query_one("#ex-resultado", Static).update(
                    "Digite um texto para buscar no nome."
                )
                return
            t0 = time.perf_counter()
            ocorrencias = sum(
                achar_substring(p.nome.lower(), texto) != []
                for p in amostra
            )
            dt = time.perf_counter() - t0
            self.screen.query_one("#ex-resultado", Static).update(
                f"{ocorrencias} nomes contêm '{texto}'  —  {dt:.6f}s"
            )

    return TreinadorApp()


def main():
    parser = argparse.ArgumentParser(description="Banco Meridian — Treinador de Algoritmos")
    parser.add_argument("csv", nargs="?", help="Caminho do CSV de clientes")
    parser.add_argument("--n", type=int, default=100_000, help="Tamanho da amostra")
    args = parser.parse_args()

    amostra = None
    if args.csv:
        amostra = carregar(Path(args.csv), limite=args.n)
    app = app_factory(amostra)
    app.run()


if __name__ == "__main__":
    main()

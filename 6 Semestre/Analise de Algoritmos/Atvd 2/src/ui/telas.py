from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header, Input, LoadingIndicator, Static
from textual.screen import Screen


class MenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="menu"):
            yield Static("Escolha uma operação do cadastro:", id="titulo")
            yield Button("1. Relatório gerencial", id="ex-ord")
            yield Button("2. Remessas fiscais", id="ex-ord-linear")
            yield Button("3. Private Banking", id="ex-topk")
            yield Button("4. Consulta central", id="ex-busca")
            yield Button("5. Cache de acesso", id="ex-indice")
            yield Button("6. Verificação pré-cadastro", id="ex-exist")
            yield Button("7. Atendimento", id="ex-prefixo")
            yield Button("8. Busca textual", id="ex-padroes")
            yield Button("Sair", id="ex-sair")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        mapa = {
"ex-ord": ("Relatório gerencial",
                       "Listar clientes do mais novo ao mais velho (campo idade) usando ordenar_idade()."),
            "ex-ord-linear": ("Remessas fiscais",
                              "Ordenar clientes por CPF usando ordenar_cpf()."),
            "ex-topk": ("Private Banking",
                        "Quais os 10 clientes com maior patrimônio? Use selecionar_topk()."),
            "ex-busca": ("Consulta central",
                         "Localizar um cliente por CPF usando buscar()."),
            "ex-indice": ("Cache de acesso",
                          "Indexar CPF -> cliente usando Indice."),
            "ex-exist": ("Verificação pré-cadastro",
                         "Antes de inserir, o CPF já existe? Use Existencia. Após executar, digite um CPF abaixo para testar."),
            "ex-prefixo": ("Atendimento",
                           "Autocomplete de nome no formulário. Use Prefixo. Após executar, digite um prefixo abaixo para ver sugestões."),
            "ex-padroes": ("Busca textual",
                           "Achar todos os nomes contendo um trecho. Use achar_substring(). Após executar, digite um texto abaixo."),
        }
        if event.button.id == "ex-sair":
            self.app.exit()
            return
        titulo, descricao = mapa[event.button.id]
        self.app.push_screen(ExercicioScreen(titulo, descricao))


class ExercicioScreen(Screen):
    def __init__(self, titulo, descricao, **kwargs):
        super().__init__(**kwargs)
        self.titulo = titulo
        self.descricao = descricao

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static(self.titulo, id="ex-titulo")
            yield Static(self.descricao, id="ex-desc")
            yield LoadingIndicator(id="ex-loading")
            yield Static("", id="ex-resultado")
            yield Input(placeholder="Digite um CPF para testar…", id="ex-input")
            yield Button("Testar CPF", id="testar")
            yield Button("Executar", id="executar")
            yield Button("Voltar", id="voltar")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#ex-loading", LoadingIndicator).display = False
        campo = self.query_one("#ex-input", Input)
        if self.titulo == "Atendimento":
            campo.placeholder = "Digite um prefixo de nome…"
            campo.display = True
        elif self.titulo == "Verificação pré-cadastro":
            campo.placeholder = "Digite um CPF para testar…"
            campo.display = True
        elif self.titulo == "Busca textual":
            campo.placeholder = "Digite um texto para buscar no nome…"
            campo.display = True
        else:
            campo.display = False
        self.query_one("#testar", Button).display = (
            self.titulo == "Verificação pré-cadastro"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "voltar":
            self.app.pop_screen()
            return
        if event.button.id == "testar":
            self.app.testar_cpf(self.query_one("#ex-input", Input).value)
            return
        self.app.executar_exercicio(self.titulo)

    def on_input_changed(self, event: Input.Changed) -> None:
        if self.titulo == "Atendimento":
            self.app.autocompletar(event.value)
        elif self.titulo == "Busca textual":
            self.app.buscar_textual(event.value)

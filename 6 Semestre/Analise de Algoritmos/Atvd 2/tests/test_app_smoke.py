from src.main import app_factory


def test_app_cria():
    app = app_factory(amostra=None)
    assert app is not None
    assert app.title == "Banco Meridian — Treinador de Algoritmos"

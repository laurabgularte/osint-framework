from src.osint_engine.loader import load_plugins

def test_plugin_loader():
    plugins = load_plugins("modules")
    assert len(plugins) > 0, "O carregador de plugins deve carregar os módulos da pasta modules/."
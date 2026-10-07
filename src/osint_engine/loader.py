import sys
import importlib
import pkgutil
from pathlib import Path
from typing import List, Type

# Adiciona a raiz do projeto (duas pastas acima de osint_engine) ao sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from modules.base import BaseModule

def load_plugins(package_name: str = "modules") -> List[Type[BaseModule]]:
    plugins = []
    try:
        package = importlib.import_module(package_name)
    except ModuleNotFoundError:
        return []

    for _, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        if module_name.endswith(".base"):
            continue
        try:
            module = importlib.import_module(module_name)
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if (
                    isinstance(attribute, type)
                    and issubclass(attribute, BaseModule)
                    and attribute is not BaseModule
                ):
                    plugins.append(attribute)
        except Exception:
            continue

    return plugins
import importlib
import pkgutil


class DoctorCheck:
    name: str = "Unknown"
    description: str = ""

    def run(self) -> dict:
        """Returns {'status': 'PASS'|'FAIL'|'WARN', 'details': [...]}"""
        raise NotImplementedError()


def discover_checks():
    checks = []
    # Discover all modules in this package
    package = __name__
    import src.profileforge.cli.doctor as doc_pkg

    for _, module_name, _ in pkgutil.iter_modules(doc_pkg.__path__):
        if module_name == "__init__":
            continue
        try:
            mod = importlib.import_module(f"{package}.{module_name}")
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, DoctorCheck)
                    and attr is not DoctorCheck
                ):
                    checks.append(attr())
        except Exception as e:
            print(f"[!] Error loading doctor plugin {module_name}: {e}")

    return checks

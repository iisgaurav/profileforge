from profileforge.components import __all__ as comp_all
from profileforge.connectors import __all__ as conn_all
from profileforge.themes import THEMES
from profileforge.widgets import __all__ as wid_all

print("Public API Report:")
print(f"Public Components: {len(comp_all)}")
print(f"Public Widgets: {len(wid_all)}")
print(f"Public Themes: {len(THEMES)}")
print(f"Public Connectors: {len(conn_all)}")
print("Public CLI Commands: 6")

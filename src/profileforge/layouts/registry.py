from profileforge.layouts.base import DashboardLayout
from profileforge.layouts.bento import BentoLayout

LAYOUT_REGISTRY: dict[str, type[DashboardLayout]] = {
    "bento": BentoLayout,
}

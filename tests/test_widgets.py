from typing import Any

import profileforge.widgets  # noqa: F401
from profileforge.components.layout import Component
from profileforge.components.widgets import Card, Text
from profileforge.core.context import BuildContext, Services
from profileforge.core.models import (
    DashboardConfig,
    MetricsConfig,
    Outputs,
    ProfileForgeConfig,
    WidgetConfig,
)
from profileforge.core.registry import WIDGET_REGISTRY
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


class SampleLifecycleWidget(Widget):
    def __init__(self):
        self.lifecycle_log = []

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="sample_widget",
            name="Sample Widget",
            category=WidgetCategory.UTILITY,
            description="A sample widget for testing the full lifecycle",
            version="1.0.0",
            author="Tester",
            tags=["sample", "test"],
            required_connectors=["local"],
        )

    def validate(self, context: BuildContext) -> None:
        self.lifecycle_log.append("validate")

    def resolve_connectors(self, context: BuildContext) -> dict[str, Any]:
        self.lifecycle_log.append("resolve_connectors")
        return super().resolve_connectors(context)

    def fetch(self, context: BuildContext) -> Any:
        self.lifecycle_log.append("fetch")
        return {"value": "hello world"}

    def transform(self, data: Any, context: BuildContext) -> Any:
        self.lifecycle_log.append("transform")
        return {"upper": data["value"].upper()}

    def build(self, data: Any, context: BuildContext) -> Component:
        self.lifecycle_log.append("build")
        return Card(title="Sample", child=Text(data["upper"]))

    def post_build(self, component: Component, context: BuildContext) -> Component:
        self.lifecycle_log.append("post_build")
        return component


class FailingWidget(Widget):
    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="failing_widget",
            name="Failing Widget",
            category=WidgetCategory.UTILITY,
            required_connectors=["local", "github"],
        )

    def build(self, data: Any, context: BuildContext) -> Component:
        raise ValueError("Simulated widget build failure")


def create_test_context(mock_theme) -> BuildContext:
    config = ProfileForgeConfig(
        version=1,
        project_name="Test Project",
        project_title="Test Title",
        active_theme="test-theme",
        widgets=[WidgetConfig(name="about")],
        connectors_config={},
        outputs=Outputs(),
        dashboard=DashboardConfig(),
        metrics=MetricsConfig(),
    )
    services = Services(connectors={})
    return BuildContext(theme=mock_theme, config=config, services=services)


def test_widget_metadata_dataclass():
    meta = WidgetMetadata(
        id="test_id",
        name="Test Widget",
        category=WidgetCategory.IDENTITY,
        description="A test widget",
        version="1.2.0",
        author="Author",
        tags=["tag1", "tag2"],
        required_connectors=["local"],
    )
    assert meta.id == "test_id"
    assert meta.name == "Test Widget"
    assert meta.category == "identity"
    assert meta.version == "1.2.0"
    assert meta.schema == 1
    assert meta.license == "MIT"
    assert meta.tags == ["tag1", "tag2"]
    assert meta.required_connectors == ["local"]
    assert meta.experimental is False
    assert meta.deprecated is False


def test_widget_categories():
    assert WidgetCategory.IDENTITY == "identity"
    assert WidgetCategory.STATS == "stats"
    assert WidgetCategory.PROJECTS == "projects"
    assert WidgetCategory.CAREER == "career"
    assert WidgetCategory.DEVELOPMENT == "development"
    assert WidgetCategory.CONTENT == "content"
    assert WidgetCategory.SOCIAL == "social"
    assert WidgetCategory.UTILITY == "utility"


def test_widget_lifecycle_execution(mock_theme):
    context = create_test_context(mock_theme)
    widget = SampleLifecycleWidget()
    component = widget.render_safe(context)

    assert widget.lifecycle_log == [
        "validate",
        "resolve_connectors",
        "fetch",
        "transform",
        "build",
        "post_build",
    ]
    assert isinstance(component, Card)
    assert component.title == "Sample"


def test_widget_render_safe_failure_isolation(mock_theme):
    context = create_test_context(mock_theme)
    widget = FailingWidget()

    # render_safe must isolate failures and return fallback Card without throwing
    component = widget.render_safe(context)

    assert isinstance(component, Card)
    assert component.title == "Error: Failing Widget"
    assert component.child is not None


def test_builtin_widgets_metadata():
    expected_widgets = [
        "about",
        "expertise",
        "focus",
        "roadmap",
        "github_stats",
        "github_languages",
    ]

    for name in expected_widgets:
        assert name in WIDGET_REGISTRY, f"Widget '{name}' must be registered"
        widget_cls = WIDGET_REGISTRY[name]
        widget = widget_cls()
        meta = widget.metadata()

        assert isinstance(meta, WidgetMetadata)
        assert meta.id == name
        assert meta.name
        assert meta.category in [
            WidgetCategory.IDENTITY,
            WidgetCategory.STATS,
            WidgetCategory.PROJECTS,
            WidgetCategory.CAREER,
            WidgetCategory.DEVELOPMENT,
            WidgetCategory.CONTENT,
            WidgetCategory.SOCIAL,
            WidgetCategory.UTILITY,
        ]
        assert isinstance(meta.required_connectors, list)


def test_builtin_widgets_render_safe(mock_theme):
    context = create_test_context(mock_theme)

    for name in [
        "about",
        "expertise",
        "focus",
        "roadmap",
        "github_stats",
        "github_languages",
    ]:
        widget_cls = WIDGET_REGISTRY[name]
        widget = widget_cls()
        component = widget.render_safe(context)
        assert isinstance(component, Component)

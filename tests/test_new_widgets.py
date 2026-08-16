from typing import Any
from unittest.mock import MagicMock

import profileforge.widgets  # noqa: F401
from profileforge.components.layout import Component
from profileforge.components.widgets import Card
from profileforge.connectors.github.models import GitHubLanguageStats, GitHubRepository
from profileforge.core.context import BuildContext, Services
from profileforge.core.models import (
    DashboardConfig,
    MetricsConfig,
    Outputs,
    ProfileForgeConfig,
    WidgetConfig,
)
from profileforge.core.registry import WIDGET_REGISTRY
from profileforge.render.layout import LayoutEngine
from profileforge.render.svg.renderer import SVGRenderer
from profileforge.widgets.base import WidgetCategory, WidgetMetadata
from profileforge.widgets.experience import ExperienceWidget
from profileforge.widgets.now import NowWidget
from profileforge.widgets.repositories import RepositoriesWidget
from profileforge.widgets.skills import SkillsWidget
from profileforge.widgets.social import SocialWidget


def create_test_context(mock_theme, widgets=None, connectors=None) -> BuildContext:
    config = ProfileForgeConfig(
        version=1,
        project_name="Grace Hopper",
        project_title="Computer Pioneer",
        active_theme="test-theme",
        widgets=widgets or [WidgetConfig(name="hero")],
        connectors_config={},
        outputs=Outputs(),
        dashboard=DashboardConfig(),
        metrics=MetricsConfig(),
    )
    services = Services(connectors=connectors or {})
    return BuildContext(theme=mock_theme, config=config, services=services)


class MockLocalConnector:
    def __init__(self, data_map: dict[str, Any]):
        self.data_map = data_map

    def fetch(self, request):
        return self.data_map.get(request.resource, {})






def test_social_widget_metadata():
    widget = SocialWidget()
    meta = widget.metadata()
    assert meta.id == "social"
    assert meta.name == "Social Links"
    assert meta.category == WidgetCategory.SOCIAL
    assert "local" in meta.required_connectors


def test_social_widget_transform_and_render(mock_theme):
    widget = SocialWidget()

    # Test dict input
    test_dict = {
        "github": "iisgaurav",
        "twitter": "iisgaurav_x",
        "linkedin": "in/iisgaurav",
        "website": "https://iisgaurav.dev",
        "discord": "iisgaurav#0001",
    }
    context = create_test_context(mock_theme)
    items = widget.transform(test_dict, context)
    assert len(items) == 5
    assert any("GitHub" in item["label"] for item in items)
    assert any("Twitter" in item["label"] for item in items)

    # Test list input
    test_list = [
        {"platform": "github", "username": "alice"},
        {"platform": "email", "handle": "alice@example.com"},
    ]
    items_list = widget.transform(test_list, context)
    assert len(items_list) == 2

    # Render card
    card = widget.render_safe(context)
    assert isinstance(card, Card)
    assert card.title == "Connect & Socials"

    render_node = LayoutEngine.calculate(card)
    renderer = SVGRenderer(context.get_render_context())
    svg = renderer.render(render_node)
    assert "Connect &amp; Socials" in svg


def test_skills_widget_metadata():
    widget = SkillsWidget()
    meta = widget.metadata()
    assert meta.id == "skills"
    assert meta.name == "Technical Skills"
    assert meta.category == WidgetCategory.CAREER
    assert "local" in meta.required_connectors


def test_skills_widget_transform_and_render(mock_theme):
    widget = SkillsWidget()
    context = create_test_context(mock_theme)

    # Fallback structure
    categories = widget.transform({}, context)
    assert "Languages" in categories
    assert "Python" in categories["Languages"]

    # Custom yaml data structure
    custom_skills = {
        "Languages": ["Python", "Rust", "Go"],
        "Frameworks": ["FastAPI", "React"],
        "Cloud": ["AWS", "Docker"],
    }
    transformed = widget.transform(custom_skills, context)
    assert len(transformed) == 3
    assert transformed["Languages"] == ["Python", "Rust", "Go"]

    card = widget.render_safe(context)
    assert isinstance(card, Card)
    assert card.title == "Technical Skills"

    render_node = LayoutEngine.calculate(card)
    renderer = SVGRenderer(context.get_render_context())
    svg = renderer.render(render_node)
    assert "Technical Skills" in svg
    assert "Python" in svg


def test_now_widget_metadata():
    widget = NowWidget()
    meta = widget.metadata()
    assert meta.id == "now"
    assert meta.name == "Now"
    assert meta.category == WidgetCategory.DEVELOPMENT
    assert "local" in meta.required_connectors


def test_now_widget_transform_and_render(mock_theme):
    widget = NowWidget()
    context = create_test_context(mock_theme)

    # Transform defaults
    data = widget.transform({}, context)
    assert "sections" in data
    assert len(data["sections"]) == 4

    # Custom now data
    custom_now = {
        "building": "Next-gen CLI compiler",
        "learning": "Zig & WebGPU",
        "reading": "Crafting Interpreters",
        "focus": "Compiler optimization",
        "location": "Mumbai, India",
        "updated": "August 2026",
    }
    transformed = widget.transform(custom_now, context)
    assert transformed["location"] == "Mumbai, India"
    assert transformed["updated"] == "August 2026"

    card = widget.build(transformed, context)
    assert isinstance(card, Card)
    assert card.title == "What I'm Doing Now"

    render_node = LayoutEngine.calculate(card)
    renderer = SVGRenderer(context.get_render_context())
    svg = renderer.render(render_node)
    assert "Next-gen CLI compiler" in svg
    assert "Crafting Interpreters" in svg


def test_experience_widget_metadata():
    widget = ExperienceWidget()
    meta = widget.metadata()
    assert meta.id == "experience"
    assert meta.name == "Experience"
    assert meta.category == WidgetCategory.CAREER
    assert "local" in meta.required_connectors


def test_experience_widget_transform_and_render(mock_theme):
    widget = ExperienceWidget()
    context = create_test_context(mock_theme)

    # Defaults
    exps = widget.transform([], context)
    assert len(exps) >= 2
    assert "role" in exps[0]
    assert "company" in exps[0]

    # Custom experience entries
    custom_exps = [
        {
            "role": "Principal Architect",
            "company": "NextGen Systems",
            "period": "2024 — Present",
            "description": "Architecting global real-time event bus infrastructure.",
            "highlights": [
                "Reduced P99 latency to under 5ms globally.",
                "Published 3 open-source core libraries.",
            ],
        }
    ]
    transformed = widget.transform(custom_exps, context)
    assert len(transformed) == 1
    assert transformed[0]["role"] == "Principal Architect"

    card = widget.build(transformed, context)
    assert isinstance(card, Card)
    assert card.title == "Work Experience"

    render_node = LayoutEngine.calculate(card)
    renderer = SVGRenderer(context.get_render_context())
    svg = renderer.render(render_node)
    assert "Principal Architect" in svg
    assert "NextGen Systems" in svg


def test_repositories_widget_metadata():
    widget = RepositoriesWidget()
    meta = widget.metadata()
    assert meta.id == "repositories"
    assert meta.name == "Featured Repositories"
    assert meta.category == WidgetCategory.PROJECTS
    assert "github" in meta.required_connectors


def test_repositories_widget_fetch_and_render(mock_theme):
    widget = RepositoriesWidget()

    # Mock github connector
    mock_connector = MagicMock()
    mock_connector.config = {"username": "torvalds"}
    mock_connector.get_repositories.return_value = [
        GitHubRepository(
            name="linux",
            stars=180000,
            primary_language="C",
            languages=[GitHubLanguageStats(name="C", bytes=50000000)],
            description="Linux kernel source tree",
            forks=52000,
        ),
        GitHubRepository(
            name="git",
            stars=53000,
            primary_language="C",
            languages=[GitHubLanguageStats(name="C", bytes=10000000)],
            description="Fast, scalable, distributed revision control system",
            forks=26000,
        ),
    ]

    context = create_test_context(
        mock_theme,
        widgets=[WidgetConfig(name="repositories", options={"config": {"limit": 2}})],
        connectors={"github": mock_connector},
    )

    fetched = widget.fetch(context)
    assert fetched["username"] == "torvalds"
    assert len(fetched["repos"]) == 2

    transformed = widget.transform(fetched, context)
    assert len(transformed["repos"]) == 2
    assert transformed["repos"][0]["name"] == "linux"
    assert transformed["repos"][0]["stars"] == 180000

    card = widget.render_safe(context)
    assert isinstance(card, Card)
    assert "torvalds" in card.title

    render_node = LayoutEngine.calculate(card)
    renderer = SVGRenderer(context.get_render_context())
    svg = renderer.render(render_node)
    assert "linux" in svg
    assert "180,000" in svg


def test_repositories_widget_fallback_when_unauthenticated(mock_theme):
    widget = RepositoriesWidget()
    context = create_test_context(mock_theme)

    # Empty context without github connector
    card = widget.render_safe(context)
    assert isinstance(card, Component)
    assert isinstance(card, Card)

    render_node = LayoutEngine.calculate(card)
    renderer = SVGRenderer(context.get_render_context())
    svg = renderer.render(render_node)
    assert "Featured Repositories" in svg
    assert "profileforge" in svg



def test_all_official_widgets_registered():
    official_widgets = [
        "social",
        "skills",
        "now",
        "experience",
        "repositories",
        "activity_timeline",
    ]
    for w in official_widgets:
        assert w in WIDGET_REGISTRY, f"Widget '{w}' must be present in WIDGET_REGISTRY"
        instance = WIDGET_REGISTRY[w]()
        assert isinstance(instance.metadata(), WidgetMetadata)

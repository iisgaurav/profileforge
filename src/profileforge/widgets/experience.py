__layer__ = "Layer 7 — Widgets"
from typing import Any

from profileforge.components.layout import Column, Component, Inline
from profileforge.components.style import Style
from profileforge.components.widgets import Card, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


@register_widget("experience")
class ExperienceWidget(Widget):
    """Career and work history timeline showcasing roles, companies, dates, and key highlights."""

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="experience",
            name="Experience",
            category=WidgetCategory.CAREER,
            description="Career and work history timeline showcasing roles, companies, dates, and highlights.",
            version="1.0.0",
            author="ProfileForge Team",
            tags=[
                "experience",
                "career",
                "work",
                "history",
                "timeline",
                "resume",
                "jobs",
            ],
            required_connectors=["local"],
        )

    def fetch(self, context: BuildContext) -> Any:
        connector = context.services.connectors.get("local")
        if not connector:
            return []
        try:
            request = DataRequest(resource="experience.yaml")
            return connector.fetch(request) or []
        except Exception:
            return []

    def transform(self, data: Any, context: BuildContext) -> list[dict[str, Any]]:
        raw_items = []
        if isinstance(data, dict):
            if "experience" in data and isinstance(data["experience"], list):
                raw_items = data["experience"]
            elif "jobs" in data and isinstance(data["jobs"], list):
                raw_items = data["jobs"]
            elif "history" in data and isinstance(data["history"], list):
                raw_items = data["history"]
        elif isinstance(data, list):
            raw_items = data

        experiences = []
        for item in raw_items:
            if isinstance(item, dict):
                role = item.get("role") or item.get("title") or "Software Engineer"
                company = (
                    item.get("company") or item.get("organization") or "Tech Company"
                )
                period = (
                    item.get("period")
                    or item.get("date")
                    or item.get("dates")
                    or "Present"
                )
                desc = item.get("description") or ""
                highlights = item.get("highlights") or []
                if isinstance(highlights, str):
                    highlights = [highlights]
                experiences.append(
                    {
                        "role": role,
                        "company": company,
                        "period": period,
                        "description": desc,
                        "highlights": highlights,
                    }
                )

        if not experiences:
            experiences = [
                {
                    "role": "Staff Software Engineer",
                    "company": "CloudScale Infrastructure",
                    "period": "2023 — Present",
                    "description": "Leading architecture for distributed telemetry and real-time event ingestion pipelines.",
                    "highlights": [
                        "Scaled high-throughput stream processing to 1M+ req/sec.",
                        "Mentored team of 12 engineers across systems engineering.",
                    ],
                },
                {
                    "role": "Senior Full-Stack Engineer",
                    "company": "Nexus Technologies",
                    "period": "2020 — 2023",
                    "description": "Architected modern web micro-frontends and robust asynchronous Python backends.",
                    "highlights": [
                        "Reduced end-to-end latency by 45% using efficient caching.",
                        "Created automated CI/CD pipeline reducing deployment time.",
                    ],
                },
            ]

        return experiences

    def build(self, data: Any, context: BuildContext) -> Component:
        experiences = data if isinstance(data, list) else []

        rows = []
        for i, exp in enumerate(experiences):
            role_text = Text(
                f"{exp['role']} · {exp['company']}",
                style=Style(font_size=14, font_weight="700", color="text"),
            )
            period_text = Text(
                exp["period"],
                style=Style(font_size=12, font_weight="600", color="primary"),
            )

            header_row = Inline(
                children=[role_text, period_text],
                gap=16,
                style=Style(width="fill", justify="space-between", align="center"),
            )
            rows.append(header_row)

            if exp.get("description"):
                desc_text = Text(
                    exp["description"],
                    style=Style(font_size=12, color="muted"),
                )
                rows.append(desc_text)

            for hl in exp.get("highlights", []):
                hl_text = Text(
                    f"▸ {hl}",
                    style=Style(font_size=12, color="muted"),
                )
                rows.append(hl_text)

        content = Column(
            children=rows,
            gap=16,
            style=Style(width="fill"),
        )

        return Card(
            title="Work Experience",
            child=content,
            style=Style(width=820, elevation="medium", variant="solid"),
        )

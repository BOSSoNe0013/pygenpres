import os
from dataclasses import dataclass
from string import Template

from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class SimpleTitle(SlideTemplate):
    title: str = "Simple Title"
    subtitle: str = "Subtitle"
    text_color: str = "#fff"

    def __post_init__(self):
        self.name = "Simple title"
        self.description = "A simple title slide"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"st_title", content=self.title),
            TemplateField(TemplateFieldType.TEXT, name=f"st_subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.COLOR, name=f"st_text_color", content=self.text_color),
        ]

    @property
    def content(self) -> str:
        html_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'simple_title.html'), 'r') as html_file:
            html_template = html_file.read()
        return Template(html_template).safe_substitute(html_values)

    @property
    def style(self) -> str:
        css_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'simple_title.css'), 'r') as css_file:
            css_template = css_file.read()
        return Template(css_template).safe_substitute(css_values)

    @property
    def script(self) -> str:
        return ""

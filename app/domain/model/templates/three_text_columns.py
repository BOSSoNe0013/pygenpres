import os
from dataclasses import dataclass
from string import Template

from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class ThreeTextColumns(SlideTemplate):
    title: str = "Three Text Columns"
    subtitle: str = "Subtitle"
    text_1: str = "This is the first text"
    text_2: str = "This is the second text"
    text_3: str = "This is the third text"
    text_color: str = "#fff"
    image: str = ""

    def __post_init__(self):
        self.name = "Three text columns"
        self.description = "A block of three text columns"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"ttc_title", content=self.title),
            TemplateField(TemplateFieldType.TEXT, name=f"ttc_subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"ttc_text_1", content=self.text_1),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"ttc_text_2", content=self.text_2),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"ttc_text_3", content=self.text_3),
            TemplateField(TemplateFieldType.COLOR, name=f"ttc_text_color", content=self.text_color),
        ]

    @property
    def content(self) -> str:
        html_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'three_text_columns.html'), 'r') as html_file:
            html_template = html_file.read()
        return Template(html_template).safe_substitute(html_values)

    @property
    def style(self) -> str:
        css_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'three_text_columns.css'), 'r') as css_file:
            css_template = css_file.read()
        return Template(css_template).safe_substitute(css_values)

    @property
    def script(self) -> str:
        return ""

import os
from dataclasses import dataclass
from string import Template
from typing import Optional

from app.domain.model.file import Image
from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class ImageText(SlideTemplate):
    title: str = "Image Text"
    subtitle: str = "Subtitle"
    text: str = "This is some text"
    text_color: str = "#fff"
    image: Optional[Image] = None

    def __post_init__(self):
        self.name = "Image Text"
        self.description = "A block of text with an image on the left"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"it_title", content=self.title),
            TemplateField(TemplateFieldType.TEXT, name=f"it_subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"it_text", content=self.text),
            TemplateField(TemplateFieldType.COLOR, name=f"it_text_color", content=self.text_color),
            TemplateField(TemplateFieldType.IMAGE, name=f"it_image", content=self.image)
        ]

    @property
    def content(self) -> str:
        html_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'image_text.html'), 'r') as html_file:
            html_template = html_file.read()
        return Template(html_template).safe_substitute(html_values)

    @property
    def style(self) -> str:
        css_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'image_text.css'), 'r') as css_file:
            css_template = css_file.read()
        return Template(css_template).safe_substitute(css_values)

    @property
    def script(self) -> str:
        return ""

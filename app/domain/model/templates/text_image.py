import os
from dataclasses import dataclass
from string import Template
from typing import Optional

from app.domain.model.file import Image
from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class TextImage(SlideTemplate):
    """
    Represents a slide template with a block of text and an optional image.
    It allows customization of the title, subtitle, text content, text color, and image.
    """
    title: str = "Text Image"
    subtitle: str = "Subtitle"
    text: str = "This is some text"
    text_color: str = "#fff"
    image: Optional[Image] = None

    def __post_init__(self):
        self.name = "Text Image"
        self.description = "A block of text with an image on the right"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"ti_title", content=self.title),
            TemplateField(TemplateFieldType.TEXT, name=f"ti_subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"ti_text", content=self.text),
            TemplateField(TemplateFieldType.COLOR, name=f"ti_text_color", content=self.text_color),
            TemplateField(TemplateFieldType.IMAGE, name=f"ti_image", content=self.image)
        ]

    @property
    def content(self) -> str:
        """
        Generates the HTML content for the text image slide.

        Returns: The HTML content as a string.
        """
        html_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'text_image.html'), 'r') as html_file:
            html_template = html_file.read()
        return Template(html_template).safe_substitute(html_values)

    @property
    def style(self) -> str:
        """
        Generates the CSS style for the text image slide.

        Returns: The CSS style as a string.
        """
        css_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'text_image.css'), 'r') as css_file:
            css_template = css_file.read()
        return Template(css_template).safe_substitute(css_values)

    @property
    def script(self) -> str:
        """
        Generates the JavaScript script for the text image slide.

        Returns: The JavaScript script as a string (empty in this case).
        """
        return ""

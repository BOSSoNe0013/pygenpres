"""
    PyGenPres - A Python Presentation Generator

    Copyright (C) 2025  Cyril BOSSELUT

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import os
from dataclasses import dataclass
from string import Template
from typing import Optional

from app.domain.model.file import Image
from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class ImageText(SlideTemplate):
    """
    Represents a slide template with an image and text.

    Attributes:
        title (str): The title of the slide.
        subtitle (str): The subtitle of the slide.
        text (str): The main text content of the slide.
        text_color (str): The color of the text, in hex format (e.g., "#fff").
        image (Optional[Image]): An optional image to display on the slide.
        name (str): The name of the template.
        description (str): A description of the template.
        fields (list[TemplateField]): The fields of the template.
    """
    title: str = "Image Text"
    subtitle: str = "Subtitle"
    text: str = "This is some text"
    image: Optional[Image] = None

    def __post_init__(self):
        self.name = "Image Text"
        self.description = "A block of text with an image on the left"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"title", content=self.title),
            TemplateField(TemplateFieldType.COLOR, name=f"title_text_color", content=self.title_text_color),
            TemplateField(TemplateFieldType.TEXT, name=f"subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"text", content=self.text),
            TemplateField(TemplateFieldType.COLOR, name=f"text_color", content=self.text_color),
            TemplateField(TemplateFieldType.IMAGE, name=f"image", content=self.image)
        ]

    @property
    def content(self) -> str:
        """
        Generates the HTML content for the image text slide.

        Reads the HTML template from 'image_text.html', substitutes
        the 'id' value, and returns the resulting HTML string.

        Returns:
            str: The HTML content of the slide.
        """
        html_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'image_text.html'), 'r') as html_file:
            html_template = html_file.read()
        return Template(html_template).safe_substitute(html_values)

    @property
    def style(self) -> str:
        """
        Generates the CSS style for the image text slide.

        Reads the CSS template from 'image_text.css', substitutes
        the 'id' value, and returns the resulting CSS string.

        Returns:
            str: The CSS style of the slide.
        """
        css_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'image_text.css'), 'r') as css_file:
            css_template = css_file.read()
        return Template(css_template).safe_substitute(css_values)

    @property
    def script(self) -> str:
        """
        Generates the JavaScript script for the image text slide.

        Currently, there is no JavaScript required for this template.

        Returns:
            str: An empty string, as no script is needed.
        """
        return ""

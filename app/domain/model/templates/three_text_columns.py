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

from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class ThreeTextColumns(SlideTemplate):
    title: str = "Three Text Columns"
    subtitle: str = "Subtitle"
    text_1: str = "This is the first text"
    text_2: str = "This is the second text"
    text_3: str = "This is the third text"
    image: str = ""
    """
    Represents a slide template with three text columns.
    It allows to define a title, a subtitle, three text blocks, a text color and an image.
    """

    def __post_init__(self):
        self.name = "Three text columns"
        self.description = "A block of three text columns"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"title", content=self.title),
            TemplateField(TemplateFieldType.COLOR, name=f"title_text_color", content=self.title_text_color),
            TemplateField(TemplateFieldType.TEXT, name=f"subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"text_1", content=self.text_1),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"text_2", content=self.text_2),
            TemplateField(TemplateFieldType.MARKDOWN, name=f"text_3", content=self.text_3),
            TemplateField(TemplateFieldType.COLOR, name=f"text_color", content=self.text_color),
        ]

    @property
    def content(self) -> str:
        """
        Generate the HTML content for the three text columns slide.

        :return: The HTML content as a string.
        """
        html_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'three_text_columns.html'), 'r') as html_file:
            html_template = html_file.read()
        return Template(html_template).safe_substitute(html_values)

    @property
    def style(self) -> str:
        """
        Generate the CSS style for the three text columns slide.

        :return: The CSS style as a string.
        """

        css_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'three_text_columns.css'), 'r') as css_file:
            css_template = css_file.read()
        return Template(css_template).safe_substitute(css_values)

    @property
    def script(self) -> str:
        """
        Generates the JavaScript script for the three text columns slide.

        :return: The JavaScript script as a string.
        """
        return ""

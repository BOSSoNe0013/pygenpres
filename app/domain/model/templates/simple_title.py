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
class SimpleTitle(SlideTemplate):
    """
    Represents a simple title slide template.
    It includes a title, a subtitle, and a text color.
    """
    title: str = "Simple Title"
    subtitle: str = "Subtitle"

    def __post_init__(self):
        self.name = "Simple title"
        self.description = "A simple title slide"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"title", content=self.title),
            TemplateField(TemplateFieldType.TEXT, name=f"subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.COLOR, name=f"title_text_color", content=self.title_text_color),
            TemplateField(TemplateFieldType.COLOR, name=f"text_color", content=self.text_color),
        ]

    @property
    def content(self) -> str:
        """
        Generates the HTML content for the simple title slide.

        :return: The HTML content as a string.
        """
        html_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'simple_title.html'), 'r') as html_file:
            html_template = html_file.read()
        return Template(html_template).safe_substitute(html_values)

    @property
    def style(self) -> str:
        """
        Generates the CSS style for the simple title slide.

        :return: The CSS style as a string.
        """
        css_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'simple_title.css'), 'r') as css_file:
            css_template = css_file.read()
        return Template(css_template).safe_substitute(css_values)

    @property
    def script(self) -> str:
        """
        Generates the JavaScript script for the simple title slide.
        Currently, there is no script for this template.
        :return: An empty string.
        """
        return ""

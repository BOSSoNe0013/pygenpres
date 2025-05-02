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

from app.domain.model.file import Video
from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class Video(SlideTemplate):
    """
    Represents a video slide template.
    """

    title: str = "Video"
    subtitle: str = "Subtitle"
    video: Optional[Video] = None
    controls: bool = False
    loop: bool = True
    autoplay: bool = True

    def __post_init__(self):
        self.name = "Video"
        self.description = "A video slide"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"title", content=self.title),
            TemplateField(TemplateFieldType.COLOR, name=f"title_text_color", content=self.title_text_color),
            TemplateField(TemplateFieldType.TEXT, name=f"subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.COLOR, name=f"text_color", content=self.text_color),
            TemplateField(TemplateFieldType.VIDEO, name=f"video", content=self.video),
            TemplateField(TemplateFieldType.BOOL, name=f"controls", content=self.controls),
            TemplateField(TemplateFieldType.BOOL, name=f"loop", content=self.loop),
            TemplateField(TemplateFieldType.BOOL, name=f"autoplay", content=self.autoplay),
        ]

    @property
    def style(self) -> str:
        """
        Generates the CSS style for the video slide.
        :return: The CSS style as a string.
        """
        css_values = {
            'id': self.id
        }
        with open(os.path.join(self.templates_path, 'video.css'), 'r') as css_file:
            css_template = css_file.read()
        return Template(css_template).safe_substitute(css_values)

    @property
    def script(self) -> str:
        """
        Generates the JavaScript script for the video slide.
        :return: The JavaScript script as a string.
        """
        js_values = {
            'id': self.id,
            'autoplay': 'true' if self.autoplay else 'false'
        }
        with open(os.path.join(self.templates_path, 'video.js'), 'r') as js_file:
            js_template = js_file.read()
        return Template(js_template).safe_substitute(js_values)

    @property
    def content(self) -> str:
        """
        Generates the HTML content for the video slide.
        :return: The HTML content as a string.
        """
        html_values = {
            'id': self.id,
            'controls': 'controls' if self.controls else '',
            'loop': 'loop' if self.loop else '',
        }
        with open(os.path.join(self.templates_path, 'video.html'), 'r') as html_file:
            html_template = html_file.read()
        return Template(html_template).safe_substitute(html_values)

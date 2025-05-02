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
from dataclasses import dataclass, field
from pathlib import Path
from string import Template
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel

from app.domain.model.templates.templates import Templates
from app.domain.model import ModelObject
from app.domain.model.file import Image, Video
from app.domain.model.templates import SlideTemplate, SlideTemplateResponse, TemplateFieldType
from app.domain.model.transitions import Transition, TransitionResponse


class SlideId(str):
    """
    Represents a unique identifier for a slide.
    """
    pass


class SlideResponse(BaseModel):
    """
    Represents the response model for a slide.
    """
    id: str
    title: str
    template: SlideTemplateResponse
    transition: TransitionResponse
    theme: str = ""
    description: str = ""
    background_image: Optional[Image] = None
    background_color: str = "#ffffff"
    background_color_alt: str = "#000000"
    accent_color: str = "#ff8f00"
    font_family: str = "Roboto"
    header_alignment: str = "center"
    position: int = 0


@dataclass
class Slide(ModelObject):
    """
    Represents a single slide in a presentation.

    Attributes:
        template (SlideTemplate): The template used to render the slide.
        transition (Transition): The transition effect to apply when moving to this slide.
        title (str): The title of the slide.
        description (str): A brief description of the slide's content.
    """
    template: SlideTemplate
    transition: Transition
    title: str = "New slide"
    description: str = ""
    background_image: Optional[Image] = None
    background_color: str = "#ffffff"
    background_color_alt: str = "#000000"
    accent_color: str = "#ff8f00"
    font_family: str = "Roboto"
    header_alignment: str = "center"
    theme: str = ""
    id: Optional[SlideId] = field(
        default_factory=lambda: SlideId(str(uuid4())))
    position: int = 0

    @property
    def templates_path(self) -> str:
        """
        Returns the path to the directory containing slide templates.
        """
        return os.path.join(Path.cwd(), 'res', 'slides')

    @property
    def __html_template__(self) -> str:
        """
        Reads and returns the base HTML template for a slide.
        """
        with open(
            os.path.join(self.templates_path, 'base_slide.html'), 'r'
        ) as html_file:
            html_template = html_file.read()
        return html_template

    def get_html(self, hidden: bool = True) -> str:
        """
        Generates the HTML representation of the slide.

        Args:
            hidden (bool): Whether the slide should be initially hidden (default: True).

        Returns:
            str: The HTML string representing the slide.
        """
        values = {
            field.name: field.get_html() for field in self.template.fields
        }
        for field in self.template.fields:
            if field.fx:
                values[f'{field.name}_extra_class'] = f' {field.fx['classes']}'
            else:
                values[f'{field.name}_extra_class'] = ''
        if not values.get('title'):
            values['title'] = self.title
        values['header_alignment'] = self.header_alignment
        class_list = [self.template.name.lower().replace(' ', '_')]
        if self.theme:
            class_list.append(self.theme)
        if self.position != 0 and hidden:
            class_list.append('hidden')
        else:
            class_list.append('current')
        content = Template(self.template.content).safe_substitute(values)
        return Template(self.__html_template__).safe_substitute({
            'slide_position': self.position,
            'slide_content': content,
            'header_alignment': self.header_alignment,
            'class_list': ' '.join(class_list)
        })

    def get_script(self) -> str:
        """
        Returns the JavaScript script associated with the slide's template.
        """
        return self.template.script

    def get_style(self) -> str:
        """
        Generates and returns the CSS style for the slide.
        """
        templates_values: dict = {
            field.name: field.get_html() if field.type is TemplateFieldType.IMAGE else field.content for field in self.template.fields
        }
        templates_values['background_color'] = self.background_color
        templates_values['background_color_alt'] = self.background_color_alt
        templates_values['accent_color'] = self.accent_color
        templates_values['header_alignment'] = self.header_alignment
        templates_values['slide_position'] = self.position
        values = {
            'background_color': self.background_color,
            'background_color_alt': self.background_color_alt,
            'background_image': self.background_image.data_url if self.background_image else '',
            'title_text_color': templates_values['title_text_color'] if 'title_text_color' in templates_values else '#000000',
            'text_color': templates_values['text_color'] if 'text_color' in templates_values else '#000000',
            'accent_color': self.accent_color,
            'font_family': self.font_family,
            'header_alignment': self.header_alignment,
            'slide_position': self.position,
            'transition': self.transition.get(self.position),
            'template': Template(self.template.style).safe_substitute(templates_values),
            'z_index': 500 - self.position,
        }
        with open(
            os.path.join(self.templates_path, 'base_slide.css'), 'r'
        ) as css_file:
            css_template = css_file.read()
        style = Template(css_template).safe_substitute(values)
        return style

    @classmethod
    def from_dict(cls, d: dict, infer_missing=False):
        """
        Creates a Slide instance from a dictionary.

        Args:
            :param d: The dictionary containing the slide data.
            :type d: dict
            :param infer_missing:
            :type infer_missing: bool

        Returns:
            Slide: The created Slide instance.
        """
        t_name = d.get('template').get('name').lower().replace(' ', '_')
        fields = d.get('template').get('fields')
        f = {}
        for field in fields:
            name = field.get('name')
            if name.endswith('image'):
                if isinstance(field.get('content'), dict):
                    f[name] = Image(**field.get('content'))
                else:
                    f[name] = None
            elif name.endswith('video'):
                if isinstance(field.get('content'), dict):
                    f[name] = Video(**field.get('content'))
                else:
                    f[name] = None
            else:
                f[name] = field.get('content')
        t = Templates(t_name).new_instance(**f)
        for field in fields:
            fx = field.get('fx')
            if fx:
                name = field.get('name')
                t.fields[t.fields.index(next(f for f in t.fields if f.name == name))].fx = fx
        p = super().from_dict(d, infer_missing=infer_missing)
        p.template = t
        return p

    def to_response(self) -> SlideResponse:
        """
        Converts the Slide object to a SlideResponse object.

        Returns:
            SlideResponse: The SlideResponse object representing the slide.
        """
        return SlideResponse(
            id=self.id,
            title=self.title,
            description=self.description,
            theme=self.theme,
            template=self.template.to_response(),
            transition=self.transition.to_response(),
            background_image=self.background_image,
            background_color=self.background_color,
            background_color_alt=self.background_color_alt,
            accent_color=self.accent_color,
            font_family=self.font_family,
            header_alignment=self.header_alignment,
            position=self.position
        )

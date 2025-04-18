import os
from dataclasses import dataclass, field
from pathlib import Path
from string import Template
from typing import Optional, Self
from uuid import uuid4
import json

from app.domain.model import ModelObject
from app.domain.model.slides import Slide


class PresentationId(str):
    """
    Represents the unique identifier for a Presentation.
    """
    pass


@dataclass
class Presentation(ModelObject):
    """
    Represents a presentation object containing slides, style, and scripts.

    Attributes:
        id (Optional[PresentationId]): The unique identifier of the presentation.
        title (str): The title of the presentation.
        footer (str): The footer content of the presentation.
        font_family (str): The font family used in the presentation.
        style (list[str]): A list of CSS styles for the presentation.
        scripts (list[str]): A list of JavaScript scripts for the presentation.
    """
    id: Optional[PresentationId] = field(
        default_factory=lambda: PresentationId(str(uuid4())))
    title: str = ""
    footer: str = ""
    font_family: str = "Roboto"
    style: list[str] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)

    def __post_init__(self):
        self._slides: list[Slide] = list()
        self._templates_path = os.path.join(Path.cwd(), 'res')

    @property
    def slides(self) -> list[Slide]:
        """
        Gets the list of slides in the presentation.

        Returns:
            list[Slide]: The list of slides.
        """
        return self._slides

    def add_slide(self, slide: Slide, position: Optional[int] = None):
        """
        Adds a slide to the presentation.

        Args:
            slide (Slide): The slide to add.
            position (Optional[int]): The position to insert the slide. If None, appends to the end.
        """
        if position is not None:
            self._slides.insert(position, slide)
            #update position
            for i, slide in enumerate(self._slides):
                slide.position = i
            return
        slide.position = len(self._slides)
        self._slides.append(slide)

    def move_slide(self, id: str, position: int) -> Self:
        """
        Moves a slide to a new position within the presentation.

        Args:
            id (str): The ID of the slide to move.
            position (int): The new position for the slide.

        Returns:
            Self: The updated Presentation object.
        """
        slide = [s for s in self._slides if s.id == id][0]
        self._slides.remove(slide)
        self._slides.insert(position, slide)
        for i, slide in enumerate(self._slides):
            slide.position = i
        return self

    def remove_slide(self, id: str):
        """
        Removes a slide from the presentation.

        Args:
            id (str): The ID of the slide to remove.
        Returns:
            Self: The updated Presentation object.
        """
        slide = [s for s in self._slides if s.id == id][0]
        self._slides.remove(slide)
        for i, slide in enumerate(self._slides):
            slide.position = i
        return self

    def update_slide(self, slide: Slide):
        """
        Updates a slide in the presentation.

        Args:
            slide (Slide): The updated slide object.
        """
        if len(self._slides) > slide.position:
            self._slides[slide.position] = slide

    def to_dict(self, encode_json=False):
        """
        Converts the presentation object to a dictionary.

        Args:
            encode_json (bool): Whether to encode the dictionary to JSON.

        Returns:
            dict: The dictionary representation of the presentation.
        """
        d = super().to_dict(encode_json=encode_json)
        #convert slides to dict
        d['slides'] = [slide.to_dict(encode_json=encode_json) for slide in self._slides]
        return d

    @classmethod
    def from_dict(cls, d: dict, infer_missing=False):
        p = super().from_dict(d, infer_missing=infer_missing)
        p._slides = [Slide.from_dict(slide, infer_missing=infer_missing) for slide in d['slides']]
        return p

    @classmethod
    def from_json(cls, s, *, parse_float=None, parse_int=None, parse_constant=None, infer_missing=False, **kw):
        o = json.loads(s)
        return cls.from_dict(o, infer_missing=infer_missing)

    def _load_scripts(self) -> str:
        """
        Loads and formats the JavaScript scripts for the presentation.

        Returns:
            str: The formatted JavaScript code.
        """
        #load js template
        js_values = {
            'total_pages_count': len(self._slides),
            'scripts': ''.join(self.scripts),
            'slides_scripts': ''.join([slide.get_script() for slide in self.slides])
        }
        with open(os.path.join(self._templates_path, 'presentation.js'), 'r') as js_file:
            js_template = js_file.read()
        return Template(js_template).safe_substitute(js_values)

    def _load_style(self) -> str:
        """
        Loads and formats the CSS styles for the presentation.

        Returns:
            str: The formatted CSS code.
        """
        #load css template
        css_values = {
            'style': ''.join(self.style),
            'slides_style': Template(''.join([slide.get_style() for slide in self._slides])).safe_substitute({'font_family': self.font_family}),
            'font_family': self.font_family
        }
        with open(os.path.join(self._templates_path, 'presentation.css'), 'r') as css_file:
            css_template = css_file.read()
        return Template(css_template).safe_substitute(css_values)

    @property
    def __html_template__(self) -> str:
        """
        Loads the HTML template for the presentation.

        Returns:
            str: The HTML template.
        """
        with open(os.path.join(self._templates_path, 'presentation.html'), 'r') as html_file:
            html_template = html_file.read()
        return html_template

    def get_footer(self) -> str:
        """
        Loads and formats the footer content for the presentation.

        Returns:
            str: The formatted footer HTML.
        """
        #load footer template
        footer_values = {
            'footer': self.footer,
            'total_pages_count': len(self._slides)
        }
        with open(os.path.join(self._templates_path, 'presentation_footer.html'), 'r') as footer_file:
            footer_template = footer_file.read()
        return Template(footer_template).safe_substitute(footer_values)

    def get_html(self) -> str:
        """
        Generates the complete HTML for the presentation.

        Returns:
            str: The complete HTML code for the presentation.
        """
        #load all templates and generate html
        html = Template(self.__html_template__).safe_substitute({
            'style': self._load_style(),
            'script': self._load_scripts(),
            'slides': ''.join([slide.get_html() for slide in self._slides]),
            'title': self.title,
            'font_family': self.font_family.replace(' ', '+'),
            'footer': self.get_footer()
        })
        return "".join([s for s in html.strip().splitlines(True) if s.strip()])

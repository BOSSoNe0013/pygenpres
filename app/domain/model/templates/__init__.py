import os.path
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, Union
from uuid import uuid4

from markdown import markdown

from app.domain.model.file import Image, Video
from app.domain.model import ModelObject


class TemplateFieldType(str, Enum):
    """
    Enum representing the different types of fields that can be present in a
    slide template.
    """
    TEXT = 'text'
    MARKDOWN = 'markdown'
    IMAGE = 'image'
    VIDEO = 'video'
    COLOR = 'color'
    BOOL = 'bool'


class TemplateId(str):
    """
    Represents the unique identifier for a slide template.
    """
    pass


@dataclass
class TemplateField(ModelObject):
    type: TemplateFieldType
    name: str
    content: Optional[Union[str, Image, Video, bool]] = None
    """
    Represents a field within a slide template.

    Attributes:
        type (TemplateFieldType): The type of the field (e.g., text, markdown, image).
        name (str): The name of the field.
        content (Optional[Union[str, Image, Video, bool]]): The content of the field.
    """

    def get_html(self) -> str:
        """
        Generates the HTML representation of the template field's content.

        Returns:
            str: The HTML representation of the content.
                 - If content is None, returns an empty string.
                 - If type is MARKDOWN, returns the content rendered as HTML using markdown.
                 - If type is IMAGE or VIDEO, returns the data URL of the image or video.
                 - Otherwise, returns the content as is.

        """
        if self.content is None:
            return ''
        if self.type is TemplateFieldType.MARKDOWN:
            return markdown(self.content, extensions=['tables', 'extra', 'fenced_code', 'codehilite', 'nl2br', 'sane_lists'])
        if self.type is TemplateFieldType.IMAGE:
            if not isinstance(self.content, str):
                return self.content.data_url
        if self.type is TemplateFieldType.VIDEO:
            if not isinstance(self.content, str):
                return self.content.data_url
        return self.content



@dataclass
class SlideTemplate(ModelObject):
    """
    Represents a template for a slide.

    Attributes:
        id (Optional[TemplateId]): The unique identifier of the template.
        name (str): The name of the template.
        description (str): A description of the template.
        fields (list[TemplateField]): A list of fields in the template.
    Properties:
        templates_path (str): The path where template files are stored.
        content (str): The content of the template.
        style (str): The style of the template.
        script (str): The script associated with the template.
    """
    id: Optional[TemplateId] = field(
        default_factory=lambda: TemplateId(str(uuid4())))
    name: str = ""
    description: str = ""
    fields: list[TemplateField] = field(default_factory=list)

    @property
    def templates_path(self) -> str:
        return os.path.join(Path.cwd(), 'res', 'slides')

    @property
    def content(self) -> str:
        return ""

    @property
    def style(self) -> str:
        return ""

    @property
    def script(self) -> str:
        return ""

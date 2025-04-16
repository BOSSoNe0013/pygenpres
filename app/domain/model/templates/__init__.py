from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union
from uuid import uuid4

from markdown import markdown

from app.domain.model.file import Image, Video
from app.domain.model import ModelObject


class TemplateFieldType(str, Enum):
    TEXT = 'text'
    MARKDOWN = 'markdown'
    IMAGE = 'image'
    VIDEO = 'video'
    COLOR = 'color'
    BOOL = 'bool'


class TemplateId(str):
    pass


@dataclass
class TemplateField(ModelObject):
    type: TemplateFieldType
    name: str
    content: Optional[Union[str, Image, Video, bool]] = None

    def get_html(self) -> str:
        if self.content is None:
            return ''
        if self.type is TemplateFieldType.MARKDOWN:
            return markdown(self.content, extensions=['tables'])
        if self.type is TemplateFieldType.IMAGE:
            if not isinstance(self.content, str):
                return self.content.data_url
        if self.type is TemplateFieldType.VIDEO:
            if not isinstance(self.content, str):
                return self.content.data_url
        return self.content



@dataclass
class SlideTemplate(ModelObject):
    id: Optional[TemplateId] = field(
        default_factory=lambda: TemplateId(str(uuid4())))
    name: str = ""
    description: str = ""
    fields: list[TemplateField] = field(default_factory=list)

    @property
    def content(self) -> str:
        return ""

    @property
    def style(self) -> str:
        return ""

    @property
    def script(self) -> str:
        return ""

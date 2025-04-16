from dataclasses import dataclass

from app.domain.model import ModelObject


@dataclass
class File(ModelObject):
    type: str
    name: str
    content: str
    size: int


@dataclass()
class Image(File):

    @property
    def data_url(self) -> str:
        return f'data:{self.type};base64,{self.content}'


@dataclass()
class Video(File):

    @property
    def data_url(self) -> str:
        return f'data:{self.type};base64,{self.content}'

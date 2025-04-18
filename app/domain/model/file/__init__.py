from dataclasses import dataclass

from app.domain.model import ModelObject


@dataclass
class File(ModelObject):
    """
    Represents a generic file.

    Attributes:
        type (str): The MIME type of the file.
        name (str): The name of the file.
        content (str): The content of the file, typically base64 encoded.
        size (int): The size of the file in bytes.
    """
    type: str
    name: str
    content: str
    size: int


@dataclass
class Image(File):
    """
    Represents an image file.

    Inherits from File.

    Properties:
        data_url (str): A data URL representation of the image.
    """

    @property
    def data_url(self) -> str:
        """
        Generates a data URL for the image.

        Returns:
            str: The data URL.
        """
        return f'data:{self.type};base64,{self.content}'


@dataclass
class Video(File):
    """
    Represents a video file.

    Inherits from File.

    Properties:
        data_url (str): A data URL representation of the image.
    """

    @property
    def data_url(self) -> str:
        """
        Generates a data URL for the video.

        Returns:
            str: The data URL.
        """
        return f'data:{self.type};base64,{self.content}'

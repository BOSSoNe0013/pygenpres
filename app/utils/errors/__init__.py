from typing import Any


class UnsupportedFileTypeError(Exception):
    """
    Custom exception class to represent errors that occur when an unsupported file type is encountered.
    This exception is raised when a file of an unsupported type is provided.

    Attributes:
        message (str): The error message, including details about the unsupported file type.
    """
    def __init__(self, message="Unsupported file type", file_type: Any=None):
        self.message = f'{message} - Type: {file_type}'
        super().__init__(self.message)

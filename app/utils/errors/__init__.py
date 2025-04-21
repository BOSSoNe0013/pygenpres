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

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
from glob import glob
from typing import Union, List

from app.utils.errors import UnsupportedFileTypeError


def list_files(path: str, ext: Union[str, List[str]], recursive = True) -> List[str]:
    """
    Lists files in a directory with the specified extension(s). Only files with extensions can be returned.

    Args:
       path (str): The directory path to search.
       ext (str | List[str]): File extension(s) to filter.
       recursive (bool, optional): Whether to search recursively. Defaults to True.

    Returns:
       List[str]: A list of file paths matching the extensions.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The given path '{path}' does not exist.")
    if isinstance(ext, str):
        if not ext.lstrip("."):
            raise UnsupportedFileTypeError(f'Invalid extension', file_type=ext)
        ext_set = {f'.{ext.lstrip(".")}'}
    elif isinstance(ext, list):
        ext_set = {f'.{e.lstrip(".")}' for e in ext if e.strip()}
    else:
        return []
    files = glob(os.path.join(path, '**', '*.*'), recursive=recursive)
    return [p for p in files if f'.{p.split('.')[-1]}' in ext_set]

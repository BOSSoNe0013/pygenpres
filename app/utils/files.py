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

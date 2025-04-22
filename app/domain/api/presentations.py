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
from app.domain.model import Record, Records
from app.domain.model.presentation import Presentation
from app.utils.files import list_files


async def get_presentations(path: str) -> Records:
    """
    Retrieves a list of presentations from a specified directory.

    Args:
        path: The path to the directory containing presentation files (JSON).

    Returns:
        A dictionary containing a list of presentation records, each with an 'id' and 'text' (title).
    """
    records = []
    files = list_files(path, ['.json'])
    for file in files:
        with open(file, 'r') as f:
            presentation = Presentation.from_json(f.read())
        records.append(Record(id=presentation.id, text=presentation.title))
    return Records(status='success', type='presentations', total=len(files),records=records)

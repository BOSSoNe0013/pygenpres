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
from app.domain.model.templates.templates import Templates


async def get_templates() -> Records:
    """
    Retrieves a list of available templates.

    Returns:
        dict: A dictionary containing a list of template records.
              Each record has 'id' and 'text' keys.
    """
    records = []
    for template in Templates.__members__.values():
        records.append(Record(id=template, text=' '.join([word.capitalize() for word in template.split('_')])))
    return Records(status='success', type='templates', total=len(records),records=records)

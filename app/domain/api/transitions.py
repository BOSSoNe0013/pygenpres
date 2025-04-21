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


from app.domain.model.transitions.transitions import Transitions


async def get_transitions() -> dict:
    """
    Retrieves a list of available transitions.

    Returns:
        dict: A dictionary containing a list of transition records.
    """
    records = []
    for transition in Transitions.__members__.values():
        records.append({'id': transition, 'text': ' '.join([word.capitalize() for word in transition.split('_')])})
    return {'records':records}

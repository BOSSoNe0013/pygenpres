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


from dataclasses import dataclass, field

from pydantic import BaseModel

from app.domain.model import ModelObject, FXRecords, Record


@dataclass
class FXItem(ModelObject):
    """
    Represents a single visual effect item.

    Attributes:
        id (str): Unique identifier for the effect item.
        name (str): Human-readable name of the effect item.
        classes (str): CSS classes associated with the effect item.    """
    id: str
    name: str
    classes: str

    def to_record(self) -> Record:
        """
        Converts the FXItem to a Record object.

        Returns:
            Record: A Record object representing the FXItem,
                    containing the id and name.
        """
        return Record(
            id=self.id,
            text=self.name
        )


@dataclass
class FX(ModelObject):
    """
    Represents a collection of visual effects.

    Attributes:
        name (str): The name of the effect collection (e.g., "Rainbow").
        items (dict[str, FXItem]): A dictionary mapping effect item IDs to FXItem objects,
                                  representing the individual effects within the collection.
    """
    name: str
    items: dict[str, FXItem]


class RainbowFX(FX):
    """
    Represents a collection of "Rainbow" visual effects.
    This class initializes the effects with predefined items.
    """
    def __init__(self):
        self.name = "Rainbow"
        self.items = {
            'rainbow-bg': FXItem(id='rainbow-bg', classes='rainbow rainbow-bg', name='Rainbow background'),
            'rainbow-bg-gradient': FXItem(id='rainbow-bg-gradient', classes='rainbow rainbow-bg-gradient', name='Rainbow background gradient'),
            'rainbow-border': FXItem(id='rainbow-border', classes='rainbow rainbow-border', name='Rainbow border'),
            'rainbow-text': FXItem(id='rainbow-text', classes='rainbow rainbow-text', name='Rainbow text'),
            'rainbow-text-gradient': FXItem(id='rainbow-text-gradient', classes='rainbow rainbow-text-gradient', name='Rainbow text gradient'),
            'rainbow-text-shadow': FXItem(id='rainbow-text-shadow', classes='rainbow rainbow-text-shadow', name='Rainbow text shadow'),
            'rainbow-box-shadow': FXItem(id='rainbow-box-shadow', classes='rainbow rainbow-box-shadow', name='Rainbow box shadow'),
        }


class ShineFX(FX):
    """
    Represents a collection of "Shine" visual effects.
    This class initializes the effects with predefined items.
    """
    def __init__(self):
        self.name = "Shine"
        self.items = {
            'shine-bg': FXItem(id='shine-bg', classes='shine shine-bg', name='Shine background'),
            'shine-border': FXItem(id='shine-border', classes='shine shine-border', name='Shine border'),
        }

class FXResponse(BaseModel):
    items: list[Record] = field(default_factory=list)

    @classmethod
    async def list_fx(cls) -> FXRecords:
        """
        Asynchronously retrieves a list of all available visual effects.

        This function combines effects from different collections (e.g., Rainbow, Shine)
        and returns them as a list of records.

        Returns:
            FXRecords: An object containing the status, total count, and list of effect records.
        """
        records = cls()
        rainbow_fx = RainbowFX()
        shine_fx = ShineFX()
        records.items.extend([item.to_record() for item in rainbow_fx.items.values()])
        records.items.extend([item.to_record() for item in shine_fx.items.values()])
        return FXRecords(status='success', total=len(records.items),records=records.items)

    @staticmethod
    def get_fx(id: str) -> str:
        """
        Retrieves the CSS classes for a specific visual effect item.

        Args:
            id (str): The ID of the effect item to retrieve.

        Returns:
            str: The CSS classes associated with the effect item, or an empty string if the ID is not found.
        """
        match(id.split('-')[0]):
            case 'rainbow':
                rainbow_fx = RainbowFX()
                if id not in rainbow_fx.items:
                    return ''
                return rainbow_fx.items[id].classes
            case 'shine':
                shine_fx = ShineFX()
                if id not in shine_fx.items:
                    return ''
                return shine_fx.items[id].classes
            case _:
                return ''

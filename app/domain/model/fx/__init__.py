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
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Union

from app.domain.model import ModelObject, FXRecords, Record


class FXTargetType(str, Enum):
    TEXT = 'text'
    ELEMENT = 'element'


@dataclass
class FXItem(ModelObject):
    """
    Represents a single visual effect item.

    Attributes:
        id (str): Unique identifier for the effect item.
        name (str): Human-readable name of the effect item.
        classes (str): CSS classes associated with the effect item.
        target_type (FXTargetType): Type of target element for the effect.
    """
    id: str
    name: str
    classes: str
    target_type: FXTargetType

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
            'rainbow-bg': FXItem(id='rainbow-bg', classes='rainbow rainbow-bg', name='Rainbow background',
                                 target_type=FXTargetType.ELEMENT),
            'rainbow-bg-gradient': FXItem(id='rainbow-bg-gradient', classes='rainbow rainbow-bg-gradient',
                                          name='Rainbow background gradient', target_type=FXTargetType.ELEMENT),
            'rainbow-border': FXItem(id='rainbow-border', classes='rainbow rainbow-border', name='Rainbow border',
                                     target_type=FXTargetType.ELEMENT),
            'rainbow-text': FXItem(id='rainbow-text', classes='rainbow rainbow-text', name='Rainbow text',
                                   target_type=FXTargetType.TEXT),
            'rainbow-text-gradient': FXItem(id='rainbow-text-gradient', classes='rainbow rainbow-text-gradient',
                                            name='Rainbow text gradient', target_type=FXTargetType.TEXT),
            'rainbow-text-shadow': FXItem(id='rainbow-text-shadow', classes='rainbow rainbow-text-shadow',
                                          name='Rainbow text shadow', target_type=FXTargetType.TEXT),
            'rainbow-box-shadow': FXItem(id='rainbow-box-shadow', classes='rainbow rainbow-box-shadow',
                                         name='Rainbow box shadow', target_type=FXTargetType.ELEMENT),
        }


class ShineFX(FX):
    """
    Represents a collection of "Shine" visual effects.
    This class initializes the effects with predefined items.
    """
    def __init__(self):
        self.name = "Shine"
        self.items = {
            'shine-bg': FXItem(id='shine-bg', classes='shine shine-bg', name='Shine background',
                               target_type=FXTargetType.ELEMENT),
            'shine-border': FXItem(id='shine-border', classes='shine shine-border', name='Shine border',
                                   target_type=FXTargetType.ELEMENT),
            'shine-text': FXItem(id='shine-text', classes='shine shine-text', name='Shine text',
                                   target_type=FXTargetType.TEXT),
        }

class FXResponse:

    @staticmethod
    def fx_path() -> str:
        """
        Returns the path to the directory containing effects css files.
        """
        return os.path.join(Path.cwd(), 'res', 'animations')

    @staticmethod
    async def list_fx(target_type: FXTargetType = None) -> FXRecords:
        """
        Asynchronously retrieves a list of all available visual effects.

        This function combines effects from different collections (e.g., Rainbow, Shine)
        and returns them as a list of records.

        Returns:
            FXRecords: An object containing the status, total count, and list of effect records.
        """
        records = []
        rainbow_fx = RainbowFX()
        shine_fx = ShineFX()
        records.extend([item.to_record() for item in rainbow_fx.items.values() if not target_type or item.target_type == target_type])
        records.extend([item.to_record() for item in shine_fx.items.values() if not target_type or item.target_type == target_type])
        return FXRecords(status='success', total=len(records),records=records)

    @staticmethod
    def get_fx(fx_id: str) -> Union[FXItem, None]:
        """
        Retrieves the CSS classes for a specific visual effect item.

        Args:
            fx_id (str): The ID of the effect item to retrieve.

        Returns:
            FXItem: The effect item, or an empty string if the ID is not found.
        """
        match(fx_id.split('-')[0]):
            case 'rainbow':
                rainbow_fx = RainbowFX()
                if fx_id not in rainbow_fx.items:
                    return None
                return rainbow_fx.items[fx_id]
            case 'shine':
                shine_fx = ShineFX()
                if fx_id not in shine_fx.items:
                    return None
                return shine_fx.items[fx_id]
            case _:
                return None

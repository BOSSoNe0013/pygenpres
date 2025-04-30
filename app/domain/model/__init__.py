from typing import Any, Optional

from dataclasses_json import DataClassJsonMixin

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
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    Represents an error response with a message.

    Attributes:
        message (str): The error message.
    """
    message: str


class Record(BaseModel):
    """
    Represents a single record with an ID and text.

    Attributes:
        id (str): The unique identifier for the record.
        text (str): The textual content of the record.
    """
    id: str
    text: str


class Records(BaseModel):
    """
    Represents a collection of records with status, type, and total count.

    Attributes:
        status (str): The status of the records.
        type (str): The type of the records.
        records (list[Record]): A list of Record objects.
        total (int): The total number of records.
    """
    status: str
    type: str
    records: list[Record]
    total: int


class TemplateRecords(Records):
    """
    Represents a collection of template records.

    This class inherits from `Records` and sets the `type` attribute to 'templates'.
    """
    type: str = 'templates'


class TransitionRecords(Records):
    """
    Represents a collection of transition records.

    This class inherits from `Records` and sets the `type` attribute to 'transitions'.
    """
    type: str = 'transitions'


class PresentationRecords(Records):
    """
    Represents a collection of presentation records.

    This class inherits from `Records` and sets the `type` attribute to 'presentations'.
    """
    type: str = 'presentations'


class ThemeRecords(Records):
    """
    Represents a collection of theme records.

    This class inherits from `Records` and sets the `type` attribute to 'themes'.
    """
    type: str = 'themes'


class FXRecords(Records):
    """
    Represents a collection of effects records.

    This class inherits from `Records` and sets the `type` attribute to 'fx'.
    """
    type: str = 'fx'


class ModelObject(DataClassJsonMixin):
    """
    Base class for model objects, providing utility methods for attribute access and manipulation.

    This class extends `DataClassJsonMixin` to enable easy serialization and deserialization
    of data class instances to and from JSON. It also provides methods for converting
    attribute values to lists, accessing attributes like dictionary keys, and dynamically
    setting attribute values.

    Attributes:
        Inherits attributes from `DataClassJsonMixin`.
    """

    def to_list(self, keys: list[str]) -> list[Optional[Any]]:
        """
        Converts the values of specified keys from the instance's attributes into a list. This method retrieves
        the value of each key provided in the keys list by accessing the internal `__dict__` attribute of
        the object. If a key does not exist as an attribute, it will return `None` for that key.

        :param keys: A list of strings representing the attribute names to retrieve from the instance. Each
            key should correspond to an attribute in the instance.
        :type keys: list[str]
        :return: A list containing the values of the specified attributes. If a specified key does not
            exist in the instance, its corresponding value will be `None` in the output.
        :rtype: list[Optional[Any]]
        """
        if not all(isinstance(key, str) for key in keys):
            raise TypeError("All keys must be strings")
        return [self.__dict__.get(key) for key in keys]

    @property
    def __keys__(self) -> list[str]:
        """
        This method provides access to all attribute names of the current class
        instance that are not meant to be private or protected. The names are
        retrieved dynamically by filtering the instance's internal dictionary
        to exclude attributes whose names begin with an underscore ('_'). The
        result is returned as a list of attribute names.

        :return: A list of the accessible attribute names which do not start
            with an underscore.
        :rtype: list[str]
        """
        return [k for k in self.__dict__ if k[0] != '_']

    def __getitem__(self, key: str) -> Any:
        """
        Provides functionality to access an attribute of an object using a key as if
        accessing an element of a dictionary.

        :param key: The name of the attribute to retrieve.
        :type key: str
        :return: The value of the attribute associated with the specified key.
        :rtype: Any
        """
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(f"Key '{key}' not found")

    def __setitem__(self, key: str, value: Any):
        """
        Sets the value for the specified key by dynamically assigning it as an
        attribute of the instance. If the key already exists as an attribute, its
        value will be updated to the new one provided.

        :param key: The name of the attribute to set.
        :type key: Any hashable type
        :param value: The value to assign to the specified key.
        :type value: Any
        :return: None
        """
        setattr(self, key, value)

from typing import Any, Optional

from dataclasses_json import DataClassJsonMixin


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

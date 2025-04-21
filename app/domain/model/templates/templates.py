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


from enum import Enum


class Templates(str, Enum):
    """
    Enumeration of available slide templates.
    Each template has a corresponding class that handles its specific structure and content.
    """
    SIMPLE_TITLE = 'simple_title'
    IMAGE_TEXT = 'image_text'
    TEXT_IMAGE = 'text_image'
    THREE_TEXT_COLUMNS = 'three_text_columns'
    VIDEO = 'video'
    IFRAME = 'iframe'

    def new_instance(self, **kwargs):
        """
        Creates a new instance of the corresponding template class.

        Args:
            **kwargs: Keyword arguments to be passed to the template class constructor.

        Returns:
            An instance of the corresponding template class.
        """
        match self:
            case Templates.SIMPLE_TITLE:
                from app.domain.model.templates.simple_title import SimpleTitle
                return SimpleTitle(**kwargs)
            case Templates.IMAGE_TEXT:
                from app.domain.model.templates.image_text import ImageText
                return ImageText(**kwargs)
            case Templates.TEXT_IMAGE:
                from app.domain.model.templates.text_image import TextImage
                return TextImage(**kwargs)
            case Templates.THREE_TEXT_COLUMNS:
                from app.domain.model.templates.three_text_columns import ThreeTextColumns
                return ThreeTextColumns(**kwargs)
            case Templates.VIDEO:
                from app.domain.model.templates.video import Video
                return Video(**kwargs)
            case Templates.IFRAME:
                from app.domain.model.templates.iframe import Iframe
                return Iframe(**kwargs)
            case _:
                raise ValueError(f'Unknown template: {self}')

    @classmethod
    def default(cls):
        """
        Returns a default template instance.

        Returns:
            An instance of the default template (SIMPLE_TITLE).
        """
        return cls.SIMPLE_TITLE.new_instance()

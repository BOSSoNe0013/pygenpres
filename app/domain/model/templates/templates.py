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

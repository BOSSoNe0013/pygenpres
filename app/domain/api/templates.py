from app.domain.model.templates.templates import Templates


async def get_templates() -> dict[str, list[dict[str, str]]]:
    """
    Retrieves a list of available templates.

    Returns:
        dict: A dictionary containing a list of template records.
              Each record has 'id' and 'text' keys.
    """
    records = []
    for template in Templates.__members__.values():
        records.append({'id': template, 'text': ' '.join([word.capitalize() for word in template.split('_')])})
    return {'records':records}

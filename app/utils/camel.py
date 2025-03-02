from fastapi_restful.camelcase import snake2camel


def to_camel(field_name: str) -> str:
    return snake2camel(field_name, True)

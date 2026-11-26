import typing

from odoo import fields, models


def rel[T: models.BaseModel](
    field: fields.Field[models.BaseModel]
) -> fields.Field[T]:  # pyright: ignore[reportInvalidTypeVarUse]
    return typing.cast('fields.Field[T]', field)


from . import (  # noqa: F401, E402
    property,
    property_offer,
    property_tag,
    property_type,
    res_users,
)

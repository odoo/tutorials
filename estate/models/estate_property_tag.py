from odoo import fields,models # type: ignore


class estatePropertytag(models.Model):
    _name="estate.property.tag"
    _description="Property tags"

    name=fields.Char(required=True)

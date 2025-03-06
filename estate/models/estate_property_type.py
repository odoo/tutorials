from odoo import fields,models # type: ignore

class estatePropertyType(models.Model):
    _name="estate.property.type"
    _description="estate property type"

    name=fields.Char(required=True)

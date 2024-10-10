from odoo import fields, models  # type: ignore

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Ayve"

    name = fields.Char(required=True)
    
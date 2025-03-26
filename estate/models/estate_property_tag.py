from odoo import models, fields # type: ignore

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    name = fields.Char("Property Tag", required=True)
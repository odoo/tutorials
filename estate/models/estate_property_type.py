from odoo import models, fields # type: ignore

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    name = fields.Char("Property Type", required=True)
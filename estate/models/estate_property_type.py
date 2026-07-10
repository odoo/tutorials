from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.types"
    _description = "Estate Property Types"

    name = fields.Char("Property Type", required=True)

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tags"
    _description = "Tags for Property"

    name = fields.Char(string="Property Tag", required=True)

    

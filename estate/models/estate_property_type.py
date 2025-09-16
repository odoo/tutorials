from odoo import fields, models

class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "estate types"

    name = fields.Char(required = True)
    
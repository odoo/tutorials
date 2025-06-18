from odoo import fields,models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate properties types"

    name = fields.Char("Name",required=True)

    
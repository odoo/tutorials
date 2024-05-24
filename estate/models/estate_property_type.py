from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "estate property types"

    # simple fields
    name = fields.Char('Type Name', required=True)
    
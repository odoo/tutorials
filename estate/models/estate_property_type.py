from odoo import models,fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "listing for property types"

    name = fields.Char(string='Name', required=True)

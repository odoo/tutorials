
from odoo import models,fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"

    name = fields.Char('Property Type', required=True)
    number = fields.Integer('Numbers')
    
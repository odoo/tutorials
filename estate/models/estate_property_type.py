from odoo import models, fields

class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"

    name = fields.Char(required = True )
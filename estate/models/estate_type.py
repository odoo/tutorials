from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "Estate property types"


    name = fields.Char(required=True)

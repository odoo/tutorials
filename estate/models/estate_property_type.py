"""module for the estate property type model"""

from odoo import models, fields

class EstatePropertyType(models.Model):
    "Estate property type odoo model"
    _name = "estate.property.type"
    _description= "model for real estate asset types (e.g. house)"
    #
    name = fields.Char("Name", required = True)

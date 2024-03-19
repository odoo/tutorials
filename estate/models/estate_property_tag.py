"""module for the estate property tag model"""

from odoo import models, fields

class EstatePropertyTag(models.Model):
    "Estate property tag odoo model"
    _name = "estate.property.tag"
    _description= "model for real estate asset tags (e.g. house)"
    #
    name = fields.Char("Name", required = True)

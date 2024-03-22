"""module for the estate property tag model"""

from odoo import fields, models

class EstatePropertyTag(models.Model):
    "Estate property tag odoo model"
    _name = "estate.property.tag"
    _description = "real estate asset tags (e.g cozy)"
    _order = "name"
    _sql_constraints = [("unique_name", "UNIQUE(name)", "property tag names must be unique")]

    name = fields.Char("Name", required = True)
    color = fields.Integer("Color")

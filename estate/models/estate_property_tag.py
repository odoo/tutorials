from odoo import fields, models
from odoo.tools import date_utils

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'tag name must be unique.')]
    _order = "name"


    name = fields.Char(string='Tag', required=True)
    color = fields.Integer(string='Color')

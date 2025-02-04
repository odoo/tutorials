from odoo import fields, models


class PropertyTag(models.Model):
    # Model Attributes
    _name = 'estate.property.tag'
    _description = 'Property Tag Model'
    _order = 'name asc'

    # SQL Constraints
    _sql_constraints = [
		('check_unique_tag', 'UNIQUE(name)', "Property tag name must be unique.")
	]

    # Basic Fields
    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(string="Color")

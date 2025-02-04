from odoo import fields, models


class EstatepropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'property Tag'
    _order = 'name ASC'
    _sql_constraints = [
		('unique_tag', 'UNIQUE (name)', 'The tag name must be unique.')
	    ]

    name = fields.Char(required=True, string="Name")
    color = fields.Integer(string="color")

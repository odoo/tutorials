from odoo import fields, models

class PropertyTag(models.Model):
	_name = 'real.estate.property.tag'
	_description = "Real Estate Property Tags Table"

	name = fields.Char("Property Tag", required=True)

from odoo import fields, models

class EstatePropertyTag(models.Model):
	_name = 'estate.property.tag'
	_description = "Property tags"

	name = fields.Char(
		string="Property Tag",
		required=True)

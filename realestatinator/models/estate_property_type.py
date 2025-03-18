from odoo import fields, models

class EstatePropertyType(models.Model):
	_name = 'estate.property.type'
	_description = 'real estate property type'
	# _order = 'sequence'

	name = fields.Char('Name', required=True)

from odoo import fields, models

class EstatePropertyType(models.Model):
	_name = 'estate.property.type'
	_description = 'real estate property type'
	_sql_constraints = [
		('name_unique', 'UNIQUE (name)', 'make sure type name is unique.')
	]	
	# _order = 'sequence'

	name = fields.Char('Name', required=True)

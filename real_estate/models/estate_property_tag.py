from odoo import fields, models


class EstatePropertyTag(models.Model):
	_name = 'estate.property.tag'
	_description = "Property tags"
	_order = 'name'

	name = fields.Char(string="Property Tag",required=True)
	color = fields.Integer("Color Index", default=0)
	#Constraints
	_sql_constraints = [
		('check_name', 'unique(name)', 'Property Tag must be UNIQUE.')
	]

from odoo import fields, models


class EstatePropertyType(models.Model):
	_name = 'estate.property.type'
	_description = "Property Type"
	_order = 'sequence'

	name = fields.Char(string="Property Type", required=True)
	sequence = fields.Integer('Sequence', default=1, help="Used to order property. Lower is better.")
	property_ids = fields.One2many('estate.property', 'property_type_id', string= "Properties") 

	#Constraints
	_sql_constraints = [
		('check_name', 'unique(name)', ('Property Type must be UNIQUE.'))
	]

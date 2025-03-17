from odoo import fields, models

class EstatePropery(models.Model):
	_name = 'estate_property'
	_description = 'real estate property'
	_order = 'sequence'

	sequence = fields.Integer('Sequence', default=0)
	name = fields.Char(required=True)
	description = fields.Text()
	postcode = fields.Char()
	date_availability = fields.Date()
	expected_price = fields.Float()
	selling_price = fields.Float()
	bedrooms = fields.Integer()
	living_area = fields.Integer()
	facades = fields.Integer()
	garage = fields.Boolean()
	garden = fields.Boolean()
	garden_area = fields.Integer()
	garden_orientation = fields.Selection(string='Orientation', selection=[('N', 'N'), ('S', 'S'), ('E', 'E'), ('W', 'W')])
	

from odoo import fields, models

class EstatePropery(models.Model):
	_name = 'estate_property'
	_description = 'real estate property'
	_order = 'sequence'

	sequence = fields.Integer('Sequence', default=0)
	name = fields.Char('Name', required=True, translate=True)
	

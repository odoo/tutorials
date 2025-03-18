from odoo import api, fields, models

class EstatePropertyType(models.Model):
	_name = 'estate.property.type'
	_description = 'real estate property type'
	_order = 'name, sequence'
	_sql_constraints = [
		('name_unique', 'UNIQUE (name)', 'make sure type name is unique.')
	]	
	
	name = fields.Char('Name', required=True)
	property_ids = fields.One2many('estate_property', 'property_type_id', string='Property Type')
	sequence = fields.Integer('sequence', default=1)
	offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
	offer_count = fields.Integer(string='Offer Count', compute='_count_offers')


	@api.depends('offer_ids')
	def _count_offers(self):
		for record in self:
			record.offer_count = len(record.offer_ids)


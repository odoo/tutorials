from odoo import fields, models

class EstatePropery(models.Model):
	_name = 'estate_property'
	_description = 'real estate property'
	_order = 'sequence'

	sequence = fields.Integer('Sequence', default=0)
	name = fields.Char('Title', required=True)
	description = fields.Text('Description')
	postcode = fields.Char('Postcode')
	date_availability = fields.Date('Available Date', copy=False, default=fields.Date.add(fields.Date.today(), months=+3))
	expected_price = fields.Float('Expected Price')
	selling_price = fields.Float('Selling Price', readonly=True, copy=False)
	bedrooms = fields.Integer('Bedrooms', default=2)
	living_area = fields.Integer('Living Area')
	facades = fields.Integer('Facades')
	garage = fields.Boolean('Garage')
	garden = fields.Boolean('Garden')
	garden_area = fields.Integer('Garden Area')
	garden_orientation = fields.Selection(string='Garden Orientation', selection=[
		('N', 'North'), 
		('S', 'South'), 
		('E', 'East'), 
		('W', 'West')
	], default='N')
	active = fields.Boolean('Active', default=False)	
	state = fields.Selection(string='State', selection=[
		('new', 'New'),
		('offer_received', 'Offer Received'),
		('offer_accepted', 'Offer Accepted'),
		('sold', 'Sold'),
		('cancelled', 'Cancelled')
	], default='new')
	property_type_id = fields.Many2one('estate.property.type', string='Property Type')
	buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
	sales_person = fields.Many2one('res.users', string='Sales Person', default=lambda self: self.env.user)
	tag_ids = fields.Many2many('estate.property.tags', string='Tags')
	offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')

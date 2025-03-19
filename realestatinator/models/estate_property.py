from odoo import api, exceptions, fields, models

class EstatePropery(models.Model):
	_name = 'estate_property'
	_description = 'real estate property'
	_order = 'id desc'
	_sql_constraints = [
		('check_expected_price_positive', 'CHECK (0 < expected_price)', 'Check that the expected price is strictly positive'),
		
	]


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
	])
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
	total_area = fields.Integer('Total Area', readonly=True, compute='_compute_total_area')
	best_price = fields.Float('Best Offer', compute='_compute_best_price')

	@api.depends('living_area', 'garden_area')
	def _compute_total_area(self):
		for line in self:
			line.total_area = line.living_area + line.garden_area

	@api.depends('offer_ids.price')
	def _compute_best_price(self):
		for record in self:
			prices = [0] + record.offer_ids.mapped('price')
			record.best_price = max(prices)

	@api.onchange('garden')
	def _set_garden_properties(self):
		for record in self:
			# record.garden_orientation = 'N' if record.garden else ''
			# record.garden_area = 10 if record.garden else 0

			if record.garden:
				if record.garden_orientation not in ['N', 'E', 'W', 'S']:
					record.garden_orientation = 'N'
				if record.garden_area == 0:
					record.garden_area = 10
			else:
				record.garden_orientation = ''
				record.garden_area = 0

	def mark_cancelled(self):
		for record in self:
			if record.state == 'cancelled':
				raise exceptions.UserError('This property is already cancelled.')
				
			if record.state == 'sold':
				raise exceptions.UserError('This property cannot be cancelled because it has already been sold.')
				
			record.state = 'cancelled'
			record.active = False
	
	def mark_sold(self):

		for record in self:
			if record.state == 'sold':
				raise exceptions.UserError('This property is already sold.')

				
			if record.state == 'cancelled':
				raise exceptions.UserError('This property cannot be sold because it has already been cancelled.')
				
			record.state = 'sold'
			record.active = False

	@api.constrains('selling_price')
	def _check_selling_price(self):
		for record in self:
			if record.state not in ['offer_accepted', 'sold']:
				return
			if record.selling_price < 0.9 * record.expected_price:
				raise exceptions.ValidationError('Selling price must be at least 90% of expected price.')

	@api.ondelete(at_uninstall=False)
	def _unlink(self):
		for record in self:
			if record.state not in ['new', 'cancelled']:
				raise exceptions.UserError('Property must be either new or cancelled to be deleted.')



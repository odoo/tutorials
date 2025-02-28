from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
	_name = 'estate.property'
	_description = "Real estate propert details"
	_order = 'id desc'
	_inherit = ['mail.thread']
	# constrain
	_sql_constraints = [
		('expected_price_positive', 'CHECK (expected_price > 0.00)', "The expected price must be strictly positive."),
		('selling_price_positive', 'CHECK (selling_price > 0.00)', "The selling price must be strictly positive.")
	]

	# fields for the property details
	name = fields.Char(string="Property Name", required=True)
	description = fields.Text(string="Description")
	postcode = fields.Char(string="Postcode")
	date_availability = fields.Date(
		string="Availability Date",
		default=lambda self: fields.Date.today() + relativedelta(months=3),
		copy=False,
		help="property availability for purchase is after 3 months from current day"
	)
	expected_price = fields.Float(string="Expected price", required=True)
	selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
	bedrooms = fields.Integer(string="Bedrooms", default=2)
	living_area = fields.Integer(string="Living Area")
	facades = fields.Integer(string="Facades")
	garage = fields.Boolean(string="Garage")
	property_image = fields.Image(string="Property Image", max_width=128, max_height=128)
	garden = fields.Boolean(string="Garden")
	garden_area = fields.Integer(string="Garden Area")
	garden_orientation = fields.Selection(
		string="Garden Orientation",
		selection=[
			('north', "North"),
			('south', "South"),
			('east', "East"),
			('west', "West")
		]
	)

	# reserved field
	active = fields.Boolean(string="Global Visibility", default=True)

	stage = fields.Selection(
		string="Status",
		selection=[
			('new', "New"),
			('offer_received', "Offer Received"),
			('offer_accepted', "Offer Accepted"),
			('sold', "Sold"),
			('cancelled', "Cancelled")
		],
		default='new',
		copy=False,
		group_expand=True,
		tracking=True
	)

	# relational fields
	property_type_id = fields.Many2one(comodel_name='estate.property.type', string="Property Type")
	salesman_id = fields.Many2one(comodel_name='res.users', string="Salesman", default=lambda self: self.env.user)
	buyer_id = fields.Many2one(comodel_name='res.partner', string="Buyer", copy=False)
	tag_ids = fields.Many2many(comodel_name='estate.property.tag', string="Tags")
	offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string="Offers")
	company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self: self.env.company)

	# compute field
	total_area = fields.Integer(string="Total Area(sqm)", compute='_compute_total_area')
	best_price = fields.Float(string="Best Offer", compute='_compute_best_offer')

	# -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

	@api.depends('living_area', 'garden_area')
	def _compute_total_area(self):
		for record in self:
			record.total_area = record.living_area + record.garden_area

	@api.depends('offer_ids.price')
	def _compute_best_offer(self):
		for property in self:
			property.best_price = max(property.offer_ids.mapped('price'), default=0)

	# ------------------------------------------------------------
    # PYTHON CONSTRAINS
    # ------------------------------------------------------------

	@api.constrains('selling_price', 'expected_price')
	def _check_selling_price(self):
		for record in self:
			min_price = record.expected_price * 0.9

			if (
				not float_is_zero(record.selling_price, precision_rounding=0.01)
				and float_compare(record.selling_price, min_price, precision_rounding=0.01) == -1
			):
				raise ValidationError(
					"The selling price cannot be lower than 90% of the expected price."
				)

	# -------------------------------------------------------------------------
    # ON-CHANGE METHODS
    # -------------------------------------------------------------------------

	@api.onchange('garden')
	def onchange_set_garden_fields(self):
		if self.garden:
			self.write({
				'garden_area': 10,
				'garden_orientation': 'north'
			})	
		else:
			self.write({
				'garden_area': 0,
				'garden_orientation': ""
			})

	# -------------------------------------------------------------------------
    # CRUD OPERATIONS
    # -------------------------------------------------------------------------

	@api.model_create_multi
	def create(self, vals_list):
		"""log message at creation of the records/properties"""
		if 'stage' in vals_list and vals_list['stage'] in ['offer_accepted', 'sold', 'cancelled']:
			self._log_offer_accepted_message(vals_list['stage'])

		return super().create(vals_list)

	def write(self, vals):
		"""Restrict stage transitions and log messages accordingly."""
		for property in self:
			new_stage = vals.get('stage', property.stage)

			# Prevent changing stage to 'offer_accepted' if no offer is accepted
			if new_stage == 'offer_accepted' and not any(
				property.offer_ids.filtered(lambda offer: offer.status == 'accepted')
			):
				raise UserError("Cannot change stage to 'Offer Accepted' because no offer has been accepted yet.")

			# Prevent changing stage to 'sold' unless it's in 'offer_accepted'
			if new_stage == 'sold' and property.stage != 'offer_accepted':
				raise UserError("Cannot change stage to 'Sold' unless an offer has been accepted.")

			# Log message when the stage changes to 'offer_accepted', 'sold', or 'cancelled'
			if 'stage' in vals and new_stage in ['offer_accepted', 'sold', 'cancelled']:
				property._log_offer_accepted_message(new_stage)

		return super().write(vals)

	@api.ondelete(at_uninstall=False)
	def _unlink_if_property_not_new_cancelled(self):
		"""property delete restriction: only new or cancelled property can delete"""
		if any(property.stage not in ['new', 'cancelled'] for property in self):
			raise UserError("Only new or cancelled property can be deleted.")

	# ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

	def action_set_property_sold(self):
		self.ensure_one()
		if not self.selling_price:
			raise UserError("Property cannot sold without any offer accepted.")
		if self.stage == 'sold':
			raise UserError("Property is already Sold.")
		elif self.stage == 'cancelled':
			raise UserError("Cancelled property cannot be sold.")

		self.stage = 'sold'

	def action_set_property_cancel(self):
		self.ensure_one()
		if self.stage == 'cancelled':
			raise UserError("Property is already cancelled.")
		elif self.stage == 'sold':
			raise UserError("Sold property cannot be cancelled.")

		self.stage = 'cancelled'

	# -------------------------------------------------------------------------
    # OTHER METHODS
    # -------------------------------------------------------------------------

	def _log_offer_accepted_message(self, stage):
		"""log message in chatter"""
		for property in self:
			stage_str = 'Offer Accepted' if stage == 'offer_accepted' else stage.capitalize()
			property.message_post(
				body=f"Offer has been {stage_str} for this property!",
				message_type='comment',
				subtype_xmlid='mail.mt_comment'
			)

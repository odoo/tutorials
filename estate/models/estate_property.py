# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api 
from datetime import date, timedelta
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
	_name="estate.property"
	_description = "Real Estate Property"

	name =fields.Char(string="Property Name")
	title=fields.Char(string="Title")
	description = fields.Text(string="Description")
	postcode=fields.Char(string="Postcode")
	available_from=fields.Date(string="Available From",copy=False,default=date.today()+timedelta(days=90))
	expected_price=fields.Float(string="Expected Price",required =True)
	selling_price = fields.Float(string="Selling Price",readonly=True,copy=False)
	bedrooms=fields.Integer(string="Bedrooms",default=2)
	living_area=fields.Integer(string="Living Area(sqm)")
	facades=fields.Integer(string="Facades")
	garage=fields.Boolean(string="Garage")
	garden=fields.Boolean(string="Garden")
	garden_area=fields.Integer(string="Garden Area")
	garden_orientation=fields.Selection([
		("north","North"),
		("south","South"),
		("east","East"),
		("west","West")
	],string="Garden Orientation")
	state=fields.Selection([
		("new","New"),
		("offer_received","Offer Received"),
		("offer_accepted","Offer Accepted"),
		("sold","Sold"),
		("cancelled","Cancelled")
	],string="Status",required=True,copy=False,default="new")
	active=fields.Boolean(string="Active",default=True)
	property_type_id = fields.Many2one("estate.property.type", string="Property Type")
	buyer_id=fields.Many2one("res.partner",string="Buyer",copy=False)
	salesperson_id = fields.Many2one("res.users",string="Salesperson",default=lambda self: self.env.user)
	tag_ids = fields.Many2many("estate.property.tag", string="Tags")
	offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
	total_area=fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
	best_price = fields.Float(compute="_compute_best_price", store=True, string="Best Price")
	validity = fields.Integer(default=7, string="Validity", store=True)
	date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True, string="Date Deadline")

	_sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive."),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The selling price must be positive.")
    ]

	def action_sold(self):
		for record in self:
			if record.state == "cancelled":
				raise UserError("Cancelled properties cannot be sold!")
			record.state = "sold"
				
	def action_cancel(self):
		for record in self:
			if record.state == "sold":
				raise UserError("Sold properties cannot be cancelled!")
			record.state = "cancelled"
				
	@api.depends("living_area","garden_area")
	def _compute_total_area(self):
		for record in self:
			record.total_area=record.living_area+record.garden_area

	@api.depends("offer_ids.price")
	def _compute_best_price(self):
		for record in self:
			record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

	@api.onchange("garden")
	def _onchange_garden(self):
		if self.garden:
			self.garden_area = 10
			self.garden_orientation = "north"
		else:
			self.garden_area = 0
			self.garden_orientation = False
	
	@api.constrains("selling_price","expected_price")
	def _check_selling_price(self):
		for record in self:
			if float_is_zero(record.selling_price,precision_digits=2):
				continue

			min_price=record.expected_price*0.9
			if float_compare(record.selling_price,min_price,precision_digits=2)==-1:
				raise ValidationError("The selling price cannot be lower than 90% of the expected price.")


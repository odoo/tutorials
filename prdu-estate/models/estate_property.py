from odoo import fields, models
from dateutil.relativedelta import relativedelta


class estateProperty(models.Model):
	_name = "estate.property"
	_description = "Unreal estate moves a lot more than real one"
	name = fields.Char(required=True)
	description = fields.Text()
	postcode = fields.Char()
	date_availability = fields.Date("Available From", copy=False, default=lambda self: fields.Datetime.now() + relativedelta(months=3))
	expected_price = fields.Float(required=True)
	selling_price = fields.Float(readonly=True, copy=False)
	bedrooms = fields.Integer(default=2)
	living_area = fields.Integer("Living Area (m^2)")
	facades = fields.Integer()
	garage = fields.Boolean()
	garden = fields.Boolean()
	garden_area = fields.Integer()
	garden_orientation = fields.Selection(selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])
	active = fields.Boolean(default=True)
	state = fields.Selection(selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")], default='new')
	property_type_id = fields.Many2one("estate.property.type", string="Type")
	customer_id = fields.Many2one("res.partner", string="Customer", copy=False)
	salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
	property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
	offer_ids = fields.One2many("estate.property.offer","property_id")

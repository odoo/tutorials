from odoo import models, fields
from odoo.tools.date_utils import relativedelta

GARDEN_ORIENTATION = [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
PROPERTY_STATE = [("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")]


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability", copy=False, default=lambda self: fields.Date.context_today(self) + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(string="Garden Orientation",
                                          selection=GARDEN_ORIENTATION)
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(string="Status", selection=PROPERTY_STATE, required=True, copy=False, default="new")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

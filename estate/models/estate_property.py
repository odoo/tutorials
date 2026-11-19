from dateutil.relativedelta import relativedelta

from odoo import fields, models
from odoo.fields import Date


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "List of estate property"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([("new", "New"),
                                ("offer_received", "Offer Received"),
                                ("offer_accepted", "Offer Accepted"),
                                ("sold", "Sold"),
                                ("cancelled", "Cancelled")], required=True, copy=False, default="new")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False, default=Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

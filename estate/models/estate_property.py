from collections import defaultdict

from odoo import fields, models
from odoo.tools import date_utils


class EstateProperty(models.Model):
    _name: str = "estate.property"
    _active = True
    _description: str | None = None

    name: fields.Char = fields.Char()
    description: fields.Text = fields.Text()
    postcode: fields.Char = fields.Char()
    date_availability: fields.Date = fields.Date('Availability Date', copy=False, default=date_utils.add(fields.Date.today(), months=3))
    expected_price: fields.Float = fields.Float()
    selling_price: fields.Float = fields.Float(readonly=True, copy=False)
    bedroom: fields.Integer = fields.Integer(default=2)
    living_area: fields.Integer = fields.Integer()
    facades: fields.Integer = fields.Integer()
    garden: fields.Boolean = fields.Boolean()
    garden_area: fields.Integer = fields.Integer()
    garage: fields.Boolean = fields.Boolean()
    garden_orientation: fields.Selection = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string='Type',
        help="Type is used to separate Leads and Opportunities")
    state = fields.Selection(
        [(word.lower(), word) for word in ["New", "Offer Received", "Offer Accepted", "Sold", "Cancelled"]],
        copy=False,
        default="new")
    property_type_id = fields.Many2one("estate.property.type")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.uid)
    buyer_id = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

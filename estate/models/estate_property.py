import datetime

from odoo import fields, models


class Estate_Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    name = fields.Char(string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=datetime.datetime.now(),
        copy=False,
    )
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copyright=False, copy=False)
    bedrooms = fields.Integer(default=4)
    living_area = fields.Integer()
    facades = fields.Integer()
    has_garage = fields.Boolean()
    has_garden = fields.Boolean()
    active = fields.Boolean(default=True)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    status = fields.Selection(
        selection=[("new", "New"), ("offer_receieved", "Offer Recieved"), ("sold", "Sold")],
        readonly=True,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property type")

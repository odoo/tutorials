from odoo import fields, models
from datetime import date, timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate App"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: date.today() + timedelta(days=90)
    )
    expected_price = fields.Float()
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    is_garage = fields.Boolean(string="Garage")
    is_garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_reject", "Offer Rejected"),
            ("offer_accept", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", ondelete="cascade")
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        ondelete="restrict",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        ondelete="restrict",
        copy=False,
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id")

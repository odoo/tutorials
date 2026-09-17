from odoo import fields, models
import datetime


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property model test description"

    name = fields.Char(required=True)
    description = fields.Text("Description of the Estate Propert Model")
    postcode = fields.Char("Post code")
    date_availability = fields.Date(
        "Availability date",
        default=lambda self: datetime.date.today() + datetime.timedelta(days=90),
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("west", "West"),
            ("east", "East")
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")

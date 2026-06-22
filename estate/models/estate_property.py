from dateutil.relativedelta import relativedelta
from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    def _default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    property_type = fields.Many2one("estate.property.type")
    sales_person = fields.Many2one("res.users")
    buyer = fields.Many2one("res.partner")
    tag_ids = fields.Many2many("estate.property.tag")
    offers = fields.One2many("estate.property.offer", "property_id", string="offers")
    date_availability = fields.Date(
        copy=False,
        default=_default_date_availability,
        # default=lambda self: fields.Date.today() + relativedelta(months=3)
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, default=3000)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_recieved", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean(default=True)

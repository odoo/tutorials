
from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property info"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )

    property_type_id = fields.Many2one("estate.property.type")
    salesman_id = fields.Many2one("res.partner")
    buyer_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

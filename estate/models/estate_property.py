from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    active = fields.Boolean(default=True)
    bedrooms = fields.Integer(default=2)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    description = fields.Text()
    expected_price = fields.Float(required=True)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    living_area = fields.Integer()
    name = fields.Char(required=True)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    postcode = fields.Char()
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    selling_price = fields.Float(readonly=True, copy=False)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")

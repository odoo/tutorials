from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property used to buy and sell houses"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(
        default=2,
    )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_accepted", "Offer Accepted"),
            ("offer_received", "Offer Received"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
    )

    active = fields.Boolean(default=False)

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )

    salesman_id = fields.Many2one(
        'res.users',
        string="Salesman",
        default=lambda self: self.env.user,

    )

    buyer_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        copy=False,
    )

    tag_id = fields.Many2many(
        string='Tags',
        comodel_name='estate.property.tag',
    )
    property_id = fields.One2many(
        string='property',
        comodel_name='estate.property.offer',
        inverse_name='property_id',
    )

    offer_id = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
        )

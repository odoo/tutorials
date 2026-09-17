from odoo import fields, models


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.add(
            fields.Date.today(),
            months=3
        )
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    has_garage = fields.Boolean()
    has_garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new',
        required=True,
        copy=False
    )
    type_id = fields.Many2one('estate.property.type', string='Type')
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        index=True,
        copy=False
    )
    user_id = fields.Many2one('res.users',
        string='Salesperson',
        index=True,
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string='Tags')
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

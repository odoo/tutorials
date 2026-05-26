from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From", copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Type',
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True, default='new', copy=False,
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type'
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False,
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Property Tags',
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute='_compute_total_area',
    )
    best_price = fields.Float(
        string="Best Offer",
        compute='_compute_best_price',
    )

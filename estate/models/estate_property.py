from odoo import fields,models, api
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Description"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation",
        help="Select One Orientation"
    )
    active = fields.Boolean(default=False)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new'
    )

    # property Many2one realtion with type
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Types'
    )

    seller_id = fields.Many2one(
        'res.users',
        string="Salesman",
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one(
        'res.partner',
        copy=False,
        string="Buyer"
    )

    # property Many2many realtion with tag
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string="Proprty Tag"
    )

    # property One2many realtion with offer
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id'
    )

    # compute the total area by living_area and garden_area
    total_area = fields.Integer(compute="_compute_totalArea")

    # function for compute the total area
    @api.depends("living_area","garden_area")
    def _compute_totalArea(self):
        for record in self:
            print("valueeeeee: ", record)
            record.total_area = record.living_area + record.garden_area
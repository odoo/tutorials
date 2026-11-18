from odoo import fields, models
from odoo.tools import date_utils


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Property'

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        'Available From',
        copy=False,
        default=lambda _: date_utils.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        default='new',
    )
    active = fields.Boolean('Active', default=True)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
    )
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesman',
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
    )

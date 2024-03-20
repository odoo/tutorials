from odoo import fields, models


class EsateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Defines a real estate property'

    name = fields.Char('Title', required=True, index=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False, 
                                    default=lambda _: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection([
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        'Garden Orientation', required=True)
    active = fields.Boolean('Active', default=True)
    status = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], 'Status', default='new')

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')

    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)

    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

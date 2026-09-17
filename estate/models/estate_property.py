from odoo import models, fields

class Property(models.Model):
    _name = "estate_property"
    _description = "estate property model"

    name = fields.Char('Nom', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Date Availability', copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Prince', readonly=True, copy=False)
    bedrooms = fields.Integer('# Bedrooms', default=2)
    living_area = fields.Integer('# Living Areas')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean('Has Garage')
    garden = fields.Boolean('Has Garden')
    garden_area = fields.Integer('# Garden Areas')
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection=[
        ('north', 'North'), 
        ('south','South'),
        ('east','East'),
        ('west','West')
        ]
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'), 
            ('offer_received', 'Offer Received'), 
            ('offer_accepted', 'Offer accepted'), 
            ('sold', 'Sold'), 
            ('cancelled', 'Cancelled')
            ],
        required=True,
        copy=False,
        default='new'
    )

    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default= lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string="Buyer", copy=False)


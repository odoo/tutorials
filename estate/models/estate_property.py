from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(
        string='Name',
        required=True,
        default="Unknown",
    )
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        string='Date availability',
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(
        string='Expected price',
        required=True,
    )
    selling_price = fields.Float(
        string='Selling price',
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(
        string='Bedrooms',
        default=2,
    )
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=True,
        default='new',
    )
    property_type = fields.Many2one('estate_property_type', string='Property type')
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tags = fields.Many2many('estate_property_tag', string='Tags')
    offers = fields.One2many('estate_property_offer', 'property_id', string='Offers')

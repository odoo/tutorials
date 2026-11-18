from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A Free Real Estate Property"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text('Description', required=False, translate=True)

    salesman_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', required=True)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    postcode = fields.Char('Postcode', required=False, translate=True)
    date_availability = fields.Datetime('Available From', required=False, copy=False, default=fields.Datetime.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', required=False, readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', required=False, default=2)
    living_area = fields.Integer('Living area (sqm)', required=False)
    facades = fields.Integer('Facades', required=False)
    garage = fields.Boolean('Garage', required=False)
    garden = fields.Boolean('Garden', required=False)
    garden_area = fields.Integer('Garden Area (sqm)', required=False)
    garden_orientation = fields.Selection(string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Determines garden's orientation")
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], required=True, copy=False, default='new') 
    active = fields.Boolean(string='Active', default=True)

from odoo import fields, models
from datetime import date, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char('Title', required=True)
    
    description = fields.Text('Description')
    
    postcode = fields.Char('Postcode')
    
    date_availability = fields.Date('Available From', copy=False, default=date.today() + timedelta(days=90))
    
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
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    
    state = fields.Selection(
        string='Status',
        required=True,
        copy=False,
        default='new',
        selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])
    
    active = fields.Boolean('Active', default=True)

    property_type_id = fields.Many2one('estate.property.type', 'Property Type')

    buyer_id = fields.Many2one('res.partner', 'Buyer', copy=False)

    salesperson_id = fields.Many2one('res.users', 'Salesperson', default=lambda self: self.env.user)

    tag_ids = fields.Many2many('estate.property.tag')

    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    
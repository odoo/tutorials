from odoo import models,fields
from datetime import timedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'


    name = fields.Char(string='Property Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability',copy=False,default=fields.Date.today()+timedelta(days=90))
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price',readonly=True,copy=False)
    bedrooms = fields.Integer(string='Number of Bedrooms',default=2)
    living_area = fields.Integer(string='Living Area (m²)')
    facades = fields.Integer(string='Number of Facades')
    garage = fields.Boolean(string='Has Garage')
    garden = fields.Boolean(string='Has Garden',default=True)
    garden_area = fields.Integer(string='Garden Area (m²)')
    garden_orientation = fields.Char(string='Garden Orientation')
    active=fields.Boolean(string="Active",default=True)
    status = fields.Selection([ # this list contains all drop-down options
        ('new', 'New'), # (internal_value,Displayed value)
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string="Status", default='new',copy=False)

    property_type_id=fields.Many2one('estate.property.type',string="Property Type")
    #property_seller_id=fields.Many2one('estate.property.seller',string="Salesman")
    #property_buyer_id=fields.Many2one('estate.property.buyer',string="Buyer")
    property_seller_id=fields.Many2one('res.users', string="Salesman",default=lambda self: self.env.user)
    property_buyer_id = fields.Many2one('res.partner', string="Buyer",copy=False) 
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")



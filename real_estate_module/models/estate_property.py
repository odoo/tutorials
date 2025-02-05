from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(required=True, string="Name")              
    # create_uid = fields.Char(required=True)
    # create_date = fields.Char(required=True)
    postcode = fields.Char(string="Postcode")
    description = fields.Text(string="Description")                    
    # postcode = fields.Char()                      
    date_availability = fields.Date(copy=False, default=fields.Date.today, string="Available Date")              
    expected_price = fields.Float(required=True, string="Expected Price")   
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")                 
    bedrooms = fields.Integer(default=2, string="No of Bedrooms")                    
    living_area = fields.Integer(string="Living Area")                 
    facades = fields.Integer(string="Facades")                     
    garage = fields.Boolean(string="Garage?")                      
    garden = fields.Boolean(string="Garden?")                      
    garden_area = fields.Integer(string="Garden Area")                 
    garden_orientation = fields.Selection(         
        [('north', 'North'),
         ('south', 'South'),
         ('east', 'East'),
         ('west', 'West')],
         string="Garden Orientation"
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True, copy=False, default='new', string="Current State"
    )

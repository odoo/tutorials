from datetime import datetime
from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "The estate_property table stores real estate property details and metadata for transaction management."
    active = fields.Boolean(default=False)
    property_name = fields.Char(required=True, tracking=True, default="Unknown") 

    create_uid = fields.Many2one('res.users', string="Created by", readonly=True, ondelete="set null")
    create_date = fields.Datetime(string="Creation Date", readonly=True)
    write_uid = fields.Many2one('res.users', string="Updated by", readonly=True, ondelete="set null")
    write_date = fields.Datetime(string="Last Updated", readonly=True)
    last_seen = fields.Datetime(string="Last Seen", readonly=True, default=datetime.now())


    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default= (datetime.today()))
    expected_price = fields.Float(required=True, digits=(8,2))
    selling_price = fields.Float(digits=(8,2), readonly=True)

    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()

    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer()

    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('west', 'West'),
        ('east', 'East')
    ], string="Garden Orientation")

    property_state = fields.Selection([
         ('new','New'),
         ('offer received','Offer Received'),
         ('offer accepted','Offer Accepted'),
         ('sold','Sold'),
         ('cancelled','Cancelled')
    ])

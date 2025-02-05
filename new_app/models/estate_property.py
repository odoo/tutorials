from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Table"
    

    name = fields.Char(required=True)
    description = fields.Text('Description', default='bla bla bla')
    postcode = fields.Char('Postcode', default='456010')
    # date_availability = fields.Date()
    date_availability = fields.Date('Availability Date', readonly=True, copy=False, default=fields.Datetime.today() + relativedelta(days=60)) 
    expected_price = fields.Float('Expected Price', default='1500000.00', required=True)
    selling_price = fields.Float('Selling Price', default='1500000.00')
    living_area = fields.Integer('Living area', default='15465')
    facades = fields.Integer('Facades', default='4')
    bedroom = fields.Integer('Bedrooms', default='2')
    garage = fields.Boolean('Garage', default=True)
    garden = fields.Boolean('Garden', default=True)
    garden_area = fields.Integer('Garden Area', default='3456', copy=False)
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], default='north', required=True)

    # name = fields.Char(required=True)
    # description = fields.Text('Description')
    # postcode = fields.Char()
    # # date_availability = fields.Date()
    # date_availability = fields.Date('Availability Date', readonly=True, copy=False, default=fields.Datetime.today() + relativedelta(days=60)) 
    # expected_price = fields.Float('Expected Price', default='1500000.00', required=True)
    # selling_price = fields.Float('Selling Price')
    # living_area = fields.Integer('Living area')
    # facades = fields.Integer('Farcades')
    # bedroom = fields.Integer('Bedrooms', default='2')
    # garage = fields.Boolean('Garage')
    # garden = fields.Boolean('Garden')
    # garden_area = fields.Integer('Garden Area', copy=False)
    # garden_orientation = fields.Selection(
    #     string=type,
    #     selection=[
    #     ('north', 'North'),
    #     ('south', 'South'),
    #     ('east', 'East'),
    #     ('west', 'West')
    # ])


    active = fields.Boolean(default=True)          # Reserved field with default value True
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], copy=False, default='new', required=True)               # Reserved field with default state as New
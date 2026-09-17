from odoo import fields, models

class Property(models.Model):
    _name = "estate.property"
    _description  = "Estate property model"


    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price  = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms  = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'), 
            ('west', 'West')
        ],
        help="Orientation is used to define the orientation of the garden"
    )
    active = fields.Boolean("Active", default=True)  
    state =  fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required= True,
        default="new"
    )

from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real-estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        default='New',  
        copy=False, 
        selection=[('New', 'new'), ('Offer Received', 'offer received'), ('Offer Accepted', 'offer accepted'), ('Sold', 'sold'), ('Cancelled', 'cancelled')])
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('North', 'north'), ('South', 'south'), ('East', 'east'), ('West', 'west')])


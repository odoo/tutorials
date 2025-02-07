from datetime import timedelta
from odoo import models,fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default= lambda self: fields.Datetime.today() + timedelta(days=90), copy= False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy = False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()

    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south','South'),
            ('east','East'),
            ('west','West')

        ],
    )
    
    state = fields.Selection(
        string="state",
        selection=[
            ('new', 'New',),
            ('offer','Offer'),
            ('received','Received'),
            ('offer accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled')

        ],
        default = 'new',
        required = True,
        copy = False,
    )

    active = fields.Boolean(default= False)





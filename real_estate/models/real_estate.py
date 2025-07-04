from odoo import models, fields
from dateutil.relativedelta import relativedelta

class RealEstate(models.Model):
    _name = "real.estate"
    _description = "This is a real estate module"


    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Availability From",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False,)

    expected_price = fields.Float(required=True)
    selling_price  = fields.Float(readonly=True,copy=False)
    bedrooms  = fields.Integer(default=2)
    living_area  = fields.Integer(string="Living Area (sqm)")
    facades  = fields.Integer()
    garage  = fields.Boolean()
    garden  = fields.Boolean()
    garden_area  = fields.Integer()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
            ]
        )
    state = fields.Selection(
        selection=[
            ('new','New'),
            ('offer received','Offer Received'),
            ('offer accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled'),
            ],
            copy = False,
            required= True,
            default='new'
    )

from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name="estate.property"
    _description="Estate Property"

    name=fields.Char(required=True)
    description=fields.Text()
    postcode=fields.Char()
    date_availablity=fields.Date(copy=False, default=fields.Date.today()+ relativedelta(months=3))
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True, copy=False)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West'),
        ]
    )
    active=fields.Boolean(default=True)
    state=fields.Selection(
        default='new',
        copy=False,
        selection=[
            ('new','New'),
            ('offer','Offer'),
            ('received','Received'),
            ('offer_accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled'),
        ],
    )

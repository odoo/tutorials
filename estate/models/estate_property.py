from datetime import datetime,timedelta
from odoo import fields,models

class Property(models.Model):
    _name="estate.property"
    _description="Estate Property"
    
    name=fields.Char(required=True)
    description=fields.Text()
    postcode=fields.Char()
    date_availability=fields.Date('Available from',copy=False,default= fields.Date.today()+timedelta(days=+90))
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True,copy=False)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer(string="Garden Area(sqm)")
    garden_orientation=fields.Selection(
        string='Direction',
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
        ],
    )
    active=fields.Boolean(default=False)
    state=fields.Selection(
        string="State",
        selection=[
            ('new','New'),
            ('offer recieved','Offer Recieved'),
            ('offer accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled'),
        ],
        default='new',
        required=True,
        copy=False
    )

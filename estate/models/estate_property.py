from odoo import fields, models
from datetime import timedelta

class Estateproperty(models.Model):
    _name = "estate.property"
    _description = "Estate property table"

    name = fields.Char('Property Name', required=True, default="unknown")
    description = fields.Text()
    postcode= fields.Char()
    date_availability= fields.Date(copy=False, default= lambda self: fields.Datetime.today() + timedelta(days=90))
    expected_price= fields.Float(required=True)
    selling_price= fields.Float(readonly=True, copy=False)
    bedrooms= fields.Integer(default=2)
    living_area= fields.Integer()
    facades= fields.Integer()
    garage= fields.Boolean()
    garden= fields.Boolean()
    garden_area= fields.Integer()
    garden_orientation= fields.Selection(
        string='Type',
        selection=[('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state= fields.Selection(
        string='State',
        selection=[('new', 'New'),('offered_rec', 'Offer recieved'),('offer_acc', 'Offer Accepted'),('sold', 'Sold'),('cancel', 'Cancelled')],
        required=True,
        copy=False,
        default='new'
        
    )

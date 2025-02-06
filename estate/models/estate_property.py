from odoo import fields,models
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description =" Good real estate"

    name= fields.Char(required=True)
    description=fields.Text()
    postcode=fields.Char()
    date_availability = fields.Date(default= datetime.now() + timedelta(days=90))
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage= fields.Boolean()
    garden= fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation= fields.Selection(string='Garden orientation',
        selection=[
            ('North', 'North'),
            ('West', 'West'),
            ('South', 'South'),
            ('East', 'East')
        ]
    )
    active = fields.Boolean('Active', default=False)
    state= fields.Selection(selection=[('new','New'),('offer received','Offer Received'),('offer accepted','Offer Accepted'),('sold','Sold'), ('cancelled','Cancelled')],required=True, default='New',copy=False)

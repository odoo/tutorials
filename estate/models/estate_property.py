from odoo import models, fields
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property warning!"

    name = fields.Char('Name', required=True, default='Unknown')
    description = fields.Text()
    postcode = fields.Char('postcode', size=6)
    date_avaliability = fields.Date('Available date', default=(fields.Date.today() + timedelta(days=90)).strftime('%Y-%m-%d'), copy=False)
    expected_price = fields.Float('Expected price')
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')

    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        selection=[
            ('north',"North"),
            ('south', "South"), 
            ('east', "East"), 
            ('west', "West")
            ]
        )
    state = fields.Selection(
        selection=[
            ('new',"New"),
            ('offer_received', "Offer received"), 
            ('offer_accepted', "Offer accepted"), 
            ('sold', "sold"),
            ('cancelled', "Cancelled")
            ]
        )
    active = fields.Boolean(active=False)

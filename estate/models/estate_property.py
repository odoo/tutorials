from odoo import fields, models # type: ignore
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"

    
    # fields
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, string="Available From", 
                                    default=lambda self: datetime.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades =  fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Direction',
        selection=[('north', 'North'), ('south', 'South'),('east', 'East'),('west', 'West')],
        help="Direction selection from North,South,East,West")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string='State',
        copy=False,
        default='new',
       
        selection=[('new', 'New'), ('offer received', 'Offer Recieved'),('offer accepted', 'Offer Accepted'),('sold', 'Sold'),('canceled', 'Canceled')],
        help="Direction selection from North,South,East,West")
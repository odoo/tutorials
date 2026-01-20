from odoo import fields, models
from dateutil import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties to sell"

    name = fields.Char(required=True)
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        selection =[
            ('new', 'New'),
            ('offer_received','Offer Received'),
            ('offer_accepted','Offer Accepted'),
            ('sold','Sold'),
            ('canceled', 'Cancelled')],
        required = True,
        default = 'new',
        copy = False,
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.today() + relativedelta.relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer('Bedrooms',default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
            string='Orientation',
            selection=[('north', 'North'), ('south', 'South'),('east', 'East'),('west', 'West')],
            help="Orientation of the garden of the property")
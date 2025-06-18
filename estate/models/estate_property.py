from odoo import fields,models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate properties"

    name = fields.Char("Estate name",required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Date availability",default=fields.Date.today() + relativedelta(months=3),copy=False)
    expected_price = fields.Float("Expected price")
    selling_price = fields.Float("Selling price",readonly=True,copy=False)
    bedrooms = fields.Integer("Number of bedrooms",default=2)
    living_area = fields.Integer("Living area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden area")
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
        help="This Type is used to tell the garden orientation for a property"
        )
    active = fields.Boolean("Active",default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', "New"), ('offer_received', "Offer received"), ('offer_accepted', "Offer Accepted"), ('sold', "Sold"), ('cancelled', "Canceled")],
        help="This is the state of the property",
        default="new",
        required=True,
        copy=False
        )
    

from odoo import models, fields
from dateutil.relativedelta import relativedelta

class EstatePropertyModel(models.Model):
    _name = "estate.property"
    _description = "Estate property model displaying single estate property"
    
    name = fields.Char("Property Name", required=True, help="Good name of the property")
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Availability Date", copy=False, default=fields.Datetime.today() + relativedelta(days=90))
    expected_price = fields.Float("Expected Price", required=True, help="Expected price by the owner")
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Total Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection([("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],string="Garden Orientation")

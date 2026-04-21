import datetime

from odoo import models, fields
import odoo.tools.date_utils as date_utils

class Property(models.Model):
    _name = 'estate.property'
    _description = 'Test Model for the Estate App'

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Date Availability", copy=False, default=date_utils.add(fields.Date.today() + date_utils.relativedelta(months=3)))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)

    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")

    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(string="Orientation", selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])

    active = fields.Boolean("Active", default=True)
    state = fields.Selection(string="State", selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")])


from dateutil.relativedelta import relativedelta
from odoo import fields, models


class Properties(models.Model):
    _name = "estate_property"
    _description = "Properties of the estate model"

    active = fields.Boolean(default=True)
    name = fields.Char("Title", required=True)
    description = fields.Text("description")
    postcode = fields.Integer("Post code")
    date_availability = fields.Date(
        "Date availability",
        copy=False,
        default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float("Expected price", required=True)
    selling_price = fields.Float("Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer("# Bedrooms", default=2)
    living_area = fields.Integer("Living area")
    facades = fields.Integer("# facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden area", default=0)
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[("north", "North"), ("east", "East"), ("west", "West"), ("south", "South")])
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")],
        required=True,
        copy=False,
        default="new")

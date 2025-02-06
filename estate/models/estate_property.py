from datetime import timedelta
from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False,default = lambda self: fields.Datetime.today() + timedelta(days=90))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True,copy = False, default = 7000000)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        string="State",
        default = "New",
        copy = False,
        selection=[
            ("New", "New"),
            ("Offer Received", "Offer Received"),
            ("Offer Accepted", "Offer Accepted"),
            ("Sold", "Sold"),
            ("Cancelled", "Cancelled"),
        ])
    active = fields.Boolean(default = True)

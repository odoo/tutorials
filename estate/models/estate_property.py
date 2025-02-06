from datetime import timedelta

from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "test description"

    name = fields.Char("Title", required=True, default="Unknown")
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Date availability", copy=False, default=fields.Date.today() + timedelta(days=+90))
    expected_price = fields.Float("Expected price", required=True)
    selling_price = fields.Float("Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living area")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [('north','North'),
         ('south','South'),
         ('east','East'),
         ('west','West')],
        string = "Garden Orientation",
        help = "It is used to define the garden orientation"
    )
    state = fields.Selection(
        [('new', 'New'),
         ('offerreceived', 'Offer Received'),
         ('offeraccepted', 'Offer Accepted'), 
         ('sold', 'Sold'), 
         ('cancelled', 'Cancelled')
        ],
        string="State",
        default = "new"
    )
    active = fields.Boolean("Active", default=True)

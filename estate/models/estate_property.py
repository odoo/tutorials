from odoo import fields, models
from datetime import date, timedelta

class Property(models.Model):
    _name = "estate.property"
    _description = "Test description for estate.property model"

    name               = fields.Char(required=True)
    expected_price     = fields.Float(required=True)
    description        = fields.Text()
    postcode           = fields.Char()
    date_availability  = fields.Date(copy=False, default=date.today() + timedelta(days=90))
    selling_price      = fields.Float(copy=False, readonly=True)
    bedrooms           = fields.Integer(default=2)
    living_area        = fields.Integer()
    facades            = fields.Integer()
    garage             = fields.Boolean()
    garden             = fields.Boolean()
    garden_area        = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[("north","North"), ("south", "South"), ("east","East"), ("west", "West")])

    active             = fields.Boolean(default=True)
    state              = fields.Selection(
        string='State',
        selection=[("new", "New"), ("offerreceived", "Offer Received"), ("offeraccepted", "Offer accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        default="new"
    )
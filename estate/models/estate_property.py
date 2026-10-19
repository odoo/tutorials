from datetime import timedelta

from odoo import fields, models


class EstateProperty(models.Model):

    _name = 'estate.property'
    _description = 'Real Estate'

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text(default="Unknown")
    postcode = fields.Char(default="Unknown")
    date_available = fields.Date(copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True, default=0)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(default=0)
    facades = fields.Integer(default=0)
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer(default=0)
    garden_orientation = fields.Selection(
        string="garden_orientation",
        selection=[("east", "East"), ("west", "West"), ("north", "North"), ("south", "South")],
    )
    active = fields.Boolean(default=False)
    state = fields.Selection(
        string="state",
        selection=[("new", "New"),
                   ("offer_recieved", "Offer recieved"),
                   ("offer_accepted", "Offer Accepted"),
                   ("sold", "Sold"),
                   ("cancelled", "Cancelled")],
        default="new",
    )

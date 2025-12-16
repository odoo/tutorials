from odoo import models, fields
from datetime import timedelta


class buildings_model(models.Model):
    _name = "estate.buildings"
    _description = "Buildings Model"

    name = fields.Char()
    description = fields.Text()
    value = fields.Integer(readonly=True, copy=False)
    availability_date = fields.Date(
        default=fields.Date.today() + timedelta(days=90), copy=False
    )
    number_of_rooms = fields.Integer(default=2)
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        "garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
    )

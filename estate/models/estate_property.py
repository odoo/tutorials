from odoo import models, fields
from datetime import timedelta

class estateProperty(models.Model):
        _name = "estate_property"
        _description = "This is property Table."

        name = fields.Char(required=True)
        description = fields.Text()
        postcode = fields.Char()
        data_availability = fields.Date(
            default=lambda self: fields.Date.today() + timedelta(days=90),
            copy=False
        )
        expected_price = fields.Float(required=True)
        selling_price = fields.Float(readonly=True, copy=False)
        bedrooms = fields.Integer(default=2)
        living_area = fields.Integer()
        facades = fields.Integer()
        garage = fields.Boolean()
        garden = fields.Boolean()
        garden_area = fields.Integer()
        garden_orientation = fields.Selection(
            string = 'Orientation',
            selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
            help = "Garden Orientation is avialable in four faces of direction."
        )
        active = fields.Boolean(default=False)
        state = fields.Selection(
            string = 'State',
            selection = [('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
            help = "Offer available in five type.",
            required=True,
            copy=False,
            default='new' 
        )
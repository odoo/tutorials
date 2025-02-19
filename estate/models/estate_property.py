from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'model for the properties in our app'

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy = False,
        default = fields.Date.add(fields.Date.today(), months = 3)
    )
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = "Garden Orientation",
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        help = 'garden orientation is used to choose the orientation of the garden attached to the property'
    )
    active = fields.Boolean(default = True)
    state = fields.Selection(
        string = "State",
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default = 'new',
        required = True,
        copy = False,
    )

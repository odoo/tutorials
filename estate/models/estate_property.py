from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"

    active = fields.Boolean(string="Active", default=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    date_availability = fields.Date(
        string="Available From",
        default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3),
        copy=False
    )
    description = fields.Text(string="Description")
    expected_price = fields.Float(string="Expected Price", required=True)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ],
        string="Garden Orientation",
        help="Direction the garden faces"
    )
    living_area = fields.Integer(string="Living Area")
    name = fields.Char(string="Name", required=True)
    postcode = fields.Char(string="Postcode")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        string="State",
        required=True,
        default='new',
        copy=False
    )

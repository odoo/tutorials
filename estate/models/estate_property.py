from odoo import models, fields


class Estate(models.Model):
    _name = "estate_property"
    _description = "real estate management"
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_available = fields.Date(
        string="Date available",
        copy=False,
        default=fields.Datetime.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(string="State", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offerRecieved", "OfferRecieved"),
            ("offerAccepted", "OfferAccepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
        required=True,
    )

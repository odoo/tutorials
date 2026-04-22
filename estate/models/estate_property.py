from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    name = fields.Char(
        required=True,
        string="Title",
    )
    description = fields.Text(
        string="Description",
    )
    postcode = fields.Char(
        string="Postcode",
    )
    date_availability = fields.Date(
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False,
        string="Available from",
    )

    expected_price = fields.Float(
        string="Expected price",
    )
    selling_price = fields.Float(
        string="Selling price",
        readonly=True,
        copy=False,
        default_export_compatible=False,
    )

    bedrooms = fields.Integer(default=2, string="Bedrooms")
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
        help="If you don't know where West is, wait for the sun to go to sleep. Its bedroom lies West.",
    )

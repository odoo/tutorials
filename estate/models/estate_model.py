from odoo import fields, models
from datetime import timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is a Estate property model containing all the data associated with housing."

    _auto = True
    _log_access = False
    # _table = "estate.property

    name = fields.Char(string="Name", required=True, index=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From", copy=False, default=fields.Date.today() + timedelta(days=90)
    )
    expected_price = fields.Float("Expected Price", required=False)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Total Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqms)")
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("west", "West"),
            ("east", "East"),
        ],
        help="Type is used to get the garden orientation in a specific direction",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("o_received", "Offer Received"),
            ("o_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", "Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    active = fields.Boolean("Active", default=True)

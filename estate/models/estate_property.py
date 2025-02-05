from dateutil.relativedelta import relativedelta

from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(
        string="Property Name",
        required=True,
        help="Property Name"
    )
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Availability Date",
        copy=False,
        default=fields.Datetime.today() + relativedelta(days=90),
    )
    expected_price = fields.Float(
        "Expected Price",
        required=True,
        help="Expected Price"
    )
    selling_price = fields.Float(
        "Selling Price",
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(
        "Bedrooms", 
        default=2
    )
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        required=True,
        copy=False,
        default="new",
    )
    
    property_type_id=fields.Many2one(string="Property Type", comodel_name="estate.property.type"    )
    buyer=fields.Many2one(string="Buyer", comodel_name="res.partner", copy=False)
    salesperson=fields.Many2one(
        string="Salesperson",
        comodel_name="res.users",
        default=lambda self: self.env.user
    )

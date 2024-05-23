from odoo import fields, models
from odoo.tools.date_utils import add


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "description"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=add(fields.Date.today(), months=3),
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
        string="Garden orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Garden orientation is used to describe orientation of garden",
    )

    tags = fields.Many2many("estate.property.tag", string="tags")

    partner_id = fields.Many2one("res.partner", string="Partner")
    property_type = fields.Many2one("estate.property.type", string="Property Type")

    salesman = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer = fields.Many2one("res.partner", string="Buyer")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Recieved"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Canceled"),
        ],
        copy=False,
        default="new",
        required=True,
    )

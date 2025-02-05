from odoo import models, fields

GARDEN_ORIENTATION_SELECTION = [
    ("north", "North"),
    ("south", "South"),
    ("east", "East"),
    ("west", "West")
]

STATE_SELECTION = [
    ("new", "New"),
    ("offer_received", "Offer Received"),
    ("offer_accepted", "Offer Accepted"),
    ("sold", "Sold"),
    ("cancelled", "Cancelled")
]


class Property(models.Model):
    _name = "estate.property"
    _description = "Contains all properties related to estate model"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From", copy=False, default=fields.Date.add(fields.Date.today(), months=3)
    )

    property_type_id = fields.Many2one(
        string="Property Type", comodel_name="estate.property.type"
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)

    bedrooms = fields.Integer(default=2)
    facades = fields.Integer()

    living_area = fields.Integer(string="Living Area (sqm)")

    garage = fields.Boolean()

    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=GARDEN_ORIENTATION_SELECTION
    )

    buyer_id = fields.Many2one(string="Buyer", comodel_name="res.partner")
    salesperson_id = fields.Many2one(
        string="Salesperson",
        comodel_name="res.users",
        default=lambda self: self.env.user
    )

    state = fields.Selection(
        selection=STATE_SELECTION,
        required=True,
        default=STATE_SELECTION[0][0]
    )
    active = fields.Boolean(default=True)

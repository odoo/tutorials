from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char(required=True)

    property_tag_ids = fields.Many2many("estate.property.tag")

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        required=True,
    )
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)

    # Description
    description = fields.Text()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Select the orientation of the property.",
    )

    # Other Infos
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )

    # Offers
    offer_ids = fields.One2many(
        "estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )

    # Hidden
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    active = fields.Boolean(default=True)

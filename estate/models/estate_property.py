from odoo import api, fields, models


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
    best_price = fields.Float(
        string="Best Price",
        compute="_compute_best_price",
    )
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
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
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

    # Compute logic

    @api.depends("living_area", "garden", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + (
                property.garden_area if property.garden else 0
            )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        has_garden = self.garden
        self.garden_area = 10 if has_garden else 0
        self.garden_orientation = "north" if has_garden else False

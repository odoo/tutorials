from odoo import api, fields, models


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
        default="new",
        copy=False,
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
    living_area = fields.Integer(string="Living Area", default=0)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    has_garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area", default=0)
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
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

    customer_id = fields.Many2one("customer", string="Customer", copy=False)

    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
        required=True,
    )
    estate_property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="estate_property_id",
    )

    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for pe in self:
            pe.total_area = (
                pe.living_area + pe.garden_area if pe.has_garden else pe.living_area
            )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for pe in self:
            pe.best_price = max(pe.offer_ids.mapped("price")) if pe.offer_ids else None

    @api.onchange("has_garden")
    def _onchange_has_garden(self):
        if self.has_garden:
            self.garden_area = 10
            self.garden_orientation = "north"

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models  # ty: ignore[unresolved-import]


class TestModel(models.Model):
    _name = "estate.property"
    _description = "Test model for real_estate module"

    name = fields.Char(required=True, string="Title")
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.today() + relativedelta(months=3),
        string="Available From",
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("west", "West"),
            ("south", "South"),
        ],
        help="Denotes the Orientation of the garden relative to the house",
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
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area if record.living_area else 0.0) + (
                record.garden_area if record.garden_area else 0.0
            )

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            if not self.garden_area:
                self.garden_area = 10
            if not self.garden_orientation:
                self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

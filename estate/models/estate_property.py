from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")

    # def _default_Date(self):
    #     return datetime.now() + relativedelta(months=3)

    property_type_id = fields.Many2one("estate.property.type", "Type")
    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=lambda x: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    sales_man_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    property_offer_id = fields.One2many("estate.property.offer", "property_id", "Offer")
    active = fields.Boolean(string="Active", default=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
        readonly=True,
    )
    total_area = fields.Float("Total Area", compute="_compute_total")
    best_price = fields.Float("Best Price", compute="_compute_best_price")

    _check_positive_price = models.Constraint(
        "CHECK (expected_price > 0.0 AND selling_price > 0.0)",
        "price must be strictly positive",
    )

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for property in self:
            if float_is_zero(property.selling_price, precision_rounding=0.01):
                continue

            if (
                float_compare(
                    property.selling_price,
                    property.expected_price * 0.9,
                    precision_rounding=0.01,
                )
                < 0
            ):
                raise ValidationError(
                    "Selling price must be at least 90% of the expected price."
                )

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.depends("property_offer_id.price")
    def _compute_best_price(self):
        if self.property_offer_id:
            self.best_price = max(self.property_offer_id.mapped("price"))
        else:
            self.best_price = 0.0

    def action_sold(self):
        for record in self:
            if not record.property_offer_id:
                raise UserError("You cannot sell a property without an offer.")
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot set to be sold")
            record.state = "sold"

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot set to be cancelled")
            record.state = "cancelled"

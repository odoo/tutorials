from dateutil.relativedelta import relativedelta  # noqa: I001

from odoo import api, fields, models  # ty: ignore[unresolved-import]
from odoo.exceptions import UserError, ValidationError  # ty: ignore[unresolved-import]
from odoo.tools.float_utils import float_is_zero, float_compare  # ty: ignore[unresolved-import]


class TestModel(models.Model):
    _name = "estate.property"
    _description = "Test model for real_estate module"
    _order = "id desc"

    name = fields.Char(required=True, string="Title")
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.today() + relativedelta(months=3),
        string="Available From",
    )
    expected_price = fields.Float(required=True)
    _check_expected_price = models.Constraint(
        "CHECK(expected_price >= 0)", "The expected price must be non-negative"
    )
    selling_price = fields.Float(readonly=True, copy=False)
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "The selling price must be non-negative"
    )
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
        string="Status",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    # property_type_id = fields.Integer(
    #     related="property_id.property_type_id", store=True
    # )
    salesman = fields.Many2one(
        "res.users",
        string="Salesman",
    )
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company.id,
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area if record.living_area else 0.0) + (
                record.garden_area if record.garden_area else 0.0
            )

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

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

    def sold_property(self):
        for record in self:
            if all(offer.status != "accepted" for offer in self.offer_ids):
                raise ValidationError(
                    "A property cannot be sold if does not have an accepted offer"
                )
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be sold")
            else:
                record.state = "sold"
        return True

    def cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled")
            else:
                record.state = "cancelled"
        return True

    @api.constrains("selling_price")
    def _constrain_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=2)
                and float_compare(
                    record.expected_price * 0.9,
                    record.selling_price,
                    precision_digits=2,
                )
                > 0
            ):
                raise ValidationError(
                    "The Selling price cannot be below 90% of the expected price"
                )

    @api.ondelete(at_uninstall=False)
    def check_delete(self):
        if any(
            not (record.state == "new" or record.state == "cancelled")
            for record in self
        ):
            raise UserError("can only delete new or cancelled properties")

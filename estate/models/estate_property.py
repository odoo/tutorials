from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True, string="Title", trim=True, tracking=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: date.today() + timedelta(days=90),
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
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    total_area = fields.Integer(
        compute="_compute_total_area",
        string="Total Area (sqm)",
        search="_search_total_area",
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        string="Status",
        copy=False,
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", string="Property Type"
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company (Location)",
        default=lambda self: self.env.company,
        required=True,
    )
    salesperson_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_id"
    )
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0)",
            "Selling price must be positive.",
        ),
    ]

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            min_offer_price = record.expected_price * 0.9
            if (
                float_compare(record.selling_price, min_offer_price, precision_digits=3)
                < 0
            ):
                raise ValidationError(
                    f"The selling price ({record.selling_price}) cannot be lower than 90% "
                    f"of the expected price ({min_offer_price})! You must reduce the expected "
                    f"price if you want to accept this offer."
                )

    @api.onchange("garden")
    def _onchange_graden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else None

    @api.onchange("offer_ids")
    def _onchange_offer_ids(self):
        if not self.offer_ids:
            self.state = "new"
        else:
            self.state = "received"

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(
                (record.offer_ids.mapped("price")),
                default=0.0 if not record.offer_ids else None,
            )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _search_total_area(self, operator, value):
        if operator in ("=", "!=", "<", "<=", ">", ">="):
            # Use raw SQL to evaluate the sum in the database
            query = """
                SELECT id
                FROM estate_property
                WHERE (living_area + garden_area) {} %s
            """.format(operator)
            self.env.cr.execute(query, (value,))
            record_ids = [row[0] for row in self.env.cr.fetchall()]
            return [("id", "in", record_ids)]
        else:
            # Unsupported operators like 'ilike' are not suitable for numeric sums
            return [("id", "=", False)]

    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_cannot_deleted(self):
        for record in self:
            if record.state != "new" and record.state != "cancelled":
                raise UserError("Only new and cancelled properties can be deleted.")

    def action_property_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be cancelled.")
            record.state = "cancelled"
        return True

    def action_property_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled property cannot be sold.")
            record.state = "sold"
        return True

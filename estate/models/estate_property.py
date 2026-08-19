from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Availability Date",
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        copy=False,
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
        selection=[
            ("n/a", "N/A"),
            ("north", "North"),
            ("east", "East"),
            ("south", "South"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        copy=False,
    )
    active = fields.Boolean(default=True)

    # Many2one references
    type_id = fields.Many2one(comodel_name="estate.property.type")
    buyer_id = fields.Many2one(comodel_name="res.partner", copy=False)
    salesperson_id = fields.Many2one(
        comodel_name="res.users",
        default=lambda self: self.env.user,
    )

    # One2many references
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
    )

    # Many2many references
    tag_ids = fields.Many2many(
        string="Tags",
        comodel_name="estate.property.tag",
    )

    # Computed
    total_area = fields.Float(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    # On change
    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else "n/a"

    def action_property_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError(
                    "This property has already been canceled. It can not be sold!"
                )
            elif record.state == "sold":
                raise UserError(
                    "This property has already been sold. It can not be sold again!"
                )
            else:
                record.state = "sold"

    def action_property_canceled(self):
        for record in self:
            if record.state == "sold":
                raise UserError(
                    "This property has already been sold. It can not be canceled!"
                )
            elif record.state == "canceled":
                raise UserError(
                    "This property has already been canceled. It can not be canceled again!"
                )
            else:
                record.state = "canceled"

    # Constraints
    _check_expected_price = models.Constraint(
        "CHECK(expected_price >= 0)", "Expected price must be >= 0!"
    )
    _check_selling_price_positive = models.Constraint(
        "CHECK(selling_price >= 0)", "Selling price must be >= 0!"
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            if (
                not float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=2,
                )
                == 1
            ):
                raise UserError(
                    "Selling price cannot be lower than 90% of the expected price!"
                )

    # Model decorators
    @api.ondelete(at_uninstall=False)
    def _prevent_deletion_if_not_new_or_canceled(self):
        for record in self:
            if record.state not in ("new", "canceled"):
                raise UserError(
                    "You cannot delete a property unless its state is 'New' or 'Canceled'."
                )

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "Properties of the real estate"
    _order = "id desc"

    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()

    date_availability = fields.Date(
        "Available From", copy=False, default=fields.Date.today() + relativedelta(months=3)
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")

    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )

    active = fields.Boolean(default=True)

    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )

    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type"
    )
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", copy=False
    )
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    property_tag_ids = fields.Many2many(
        "estate.property.tag", string="Property tags"
    )
    property_offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers"
    )

    total_area = fields.Integer("Total area", compute="_compute_total_area")
    best_price = fields.Float("Best offer", compute="_compute_best_price")

    # constraints

    # Make sure that expected price is positive
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Expected price must be positive"
    )

    # Make sure that selling price is positive or equal to zero
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "Selling price must be positive or equal to zero"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("property_offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.property_offer_ids.mapped(
                "price")) if record.property_offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_orientation = None
            self.garden_area = 0
        else:
            self.garden_orientation = "north"
            self.garden_area = 10

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("You cannot cancel a sold property")
            record.state = "cancelled"
        return True

    def action_sell_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("You cannot sell a cancelled property")
            record.state = "sold"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_expected_to_selling(self):
        for record in self:
            # if no offer is accepted, then selling price is zero
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                raise ValidationError(
                    "The selling price is too low, it has to be at least 90% of expected price")

    # allow to delete only when states are new and cancelled
    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state != "new" and record.state != "cancelled":
                raise UserError("Can delete only new or cancelled properties")

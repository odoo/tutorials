from odoo import models, fields, api
import odoo.tools.date_utils as date_utils
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils


class Property(models.Model):
    # Private attributes
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    # Field declarations
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    tag_ids = fields.Many2many("estate.property.tag")
    type_id = fields.Many2one("estate.property.type")
    postcode = fields.Char()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    total_area = fields.Integer(compute="_compute_total_area")
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        default='south'
    )
    date_availability = fields.Date(
        copy=False,
        default=lambda x: fields.Date.today() + date_utils.relativedelta(months=3),
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    expected_price = fields.Float(required=True)
    best_offer = fields.Integer(compute="_compute_best_offer")
    selling_price = fields.Float(readonly=True, copy=False)
    buyer_id = fields.Many2one("res.partner", copy=False, readonly=True)
    salesman_id = fields.Many2one(
        "res.users",
        default=lambda self: self.env.user.id,
    )
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
    active = fields.Boolean(default=True)

    # SQL constraints and indexes
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)", "The expected price should be a positive number."
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price > 0)", "The selling_price should be a positive number."
    )

    # Compute, inverse and search methods
    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            offers = record.offer_ids.filtered(lambda offer: offer.status != "refused")
            record.best_offer = max(offers.mapped("price"), default=0)

    # Constrains methods and onchange methods
    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if (
                not float_utils.float_is_zero(record.selling_price, precision_digits=2)
                and float_utils.float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=2,
                )
                == -1
            ):
                raise ValidationError(
                    "A selling price must be at least 90% of the expected_price"
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = None

    # CRUD methods
    @api.ondelete(at_uninstall=False)
    def _delete(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError("Only new and cancelled properties can be deleted.")
        return super().unlink()

    # Action methods
    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be sold")
            record.state = "sold"

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled")

            record.state = "cancelled"

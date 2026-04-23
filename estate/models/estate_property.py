from odoo import models, fields, api
import odoo.tools.date_utils as date_utils
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    # General information
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Tags")
    type_id = fields.Many2one(comodel_name="estate.property.type", string="Type")
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
        ]
    )
    # Sales info
    date_availability = fields.Date(
        copy=False,
        default=lambda x: date_utils.add(
            fields.Date.today() + date_utils.relativedelta(months=3)
        ),
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        inverse="_compute_state",
    )
    expected_price = fields.Float(required=True)
    best_offer = fields.Integer(compute="_compute_best_offer")
    selling_price = fields.Float(readonly=True, copy=False)
    buyer_id = fields.Many2one(
        comodel_name="res.partner", string="Buyer", copy=False, readonly=True
    )
    salesman_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesman",
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

    _check_expected_price = models.Constraint("CHECK(expected_price > 0)")

    _check_selling_price = models.Constraint("CHECK(selling_price > 0)")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            offers = [
                offer.price for offer in record.offer_ids if offer.status != "refused"
            ]
            best = max([0, *offers])
            record.best_offer = best

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = None

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if (
                record.state == "offer_received"
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

    @api.depends("state", "offer_ids")
    def _compute_state(self):
        for record in self:
            if record.state not in ["sold", "cancelled"]:
                if record.offer_ids:
                    record.state = "offer_received"
                else:
                    record.state = "new"

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

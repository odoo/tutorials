from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "A property expected price must be strictly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "A property selling price must be positive",
        ),
    ]
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3)
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
        string="Type",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
        context={"no_create": True},
    )
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )
    total_area = fields.Integer(
        compute="_compute_total_area",
    )
    best_price = fields.Float(
        string="Best Price",
        compute="_compute_best_price",
    )
    image = fields.Binary(string="Image", attachment=True)

    @api.depends("living_area", "garden_area", "garden")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (
                (record.living_area or 0) + (record.garden_area or 0)
                if record.garden
                else (record.living_area or 0)
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
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_orientation = "north"
            self.garden_area = 10

    def action_sold(self):
        for record in self:
            if record.state == "sold":
                raise UserError("You cannot sell an already sold property")
            if record.state == "cancelled":
                raise UserError("Cancelled Property can't be sold")
            accepted_offer = record.offer_ids.filtered(
                lambda offer: offer.status == "accepted"
            )
            if not accepted_offer:
                raise UserError("You cannot sell a property without an accepted offer")
            record.write({"state": "sold"})

    def action_cancel(self):
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            else:
                raise UserError("Sold Property can't be cancelled")

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=2)
                and float_compare(
                    record.selling_price,
                    0.9 * record.expected_price,
                    precision_digits=2,
                )
                < 0
            ):
                raise UserError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_except_state(self):
        for record in self:
            if record.state not in ["new", "canceled"]:
                raise UserError("You cannot delete a property that is not new or canceled")

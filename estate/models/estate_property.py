from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property models"
    _order = "id desc"

    _sql_constraints = [
        (
            "expected_price_positive",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive!",
        ),
        (
            "selling_price_positive",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive!",
        ),
    ]

    name = fields.Char("Title", default="Unknown", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.today() + timedelta(days=90)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Float("Total area", compute="_compute_total_area")
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
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="new",
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one(
        "res.users", string="salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    best_offer = fields.Float("Best offer", compute="_compute_best_offer")

    # Python constraints -- selling price cannot be lower than 90% of the expected price
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=2)
                and float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=2,
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price must not be lower than 90% of the expected price!"
                )

    # Compute method
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 20
            self.garden_orientation = "north"
        else:
            self.garden_orientation = False
            self.garden_area = 0

    @api.ondelete(at_uninstall=False)
    def _prevent_deletion(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(
                    "Only properties in 'New' or 'Cancelled' state can be deleted."
                )

    #  action Methods
    def action_set_sold(self):
        if self.state == "cancelled":
            raise UserError("A cancelled property cannot be sold.")
        self.state = "sold"

    def action_set_cancelled(self):
        if self.state == "sold":
            raise UserError("A Sold property cannot to be cancelled.")
        self.state = "cancelled"

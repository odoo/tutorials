from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Realestate(models.Model):
    _name = "realestate"
    _description = "Estate"
    _order = "type_id"
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
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
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
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
    owner_id = fields.Many2one("buyer")
    type_id = fields.Many2one("types", widget="handle")
    tag_ids = fields.Many2many("tags", string="Tags")
    seller_id = fields.Many2one("seller")
    buyer_id = fields.Many2one("res.partner")
    offer_ids = fields.One2many("offer", "property_id")
    status = fields.Selection(related="offer_ids.status")
    price = fields.Float(related="offer_ids.price")
    validity = fields.Integer(related="offer_ids.validity")
    deadline = fields.Date(related="offer_ids.deadline")
    total_area = fields.Integer(compute="_compute_total")
    best_price = fields.Float(compute="_max_offer_price")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _max_offer_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_set_property_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold")
            record.state = "sold"

    def action_set_property_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be Cancelled")
            record.state = "cancelled"

    # def action_set_offer_accepted(self):
    #     for record in self:
    #         if record.status

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price> 0)",
            "Expected price must be positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price> 0)",
            "Selling price must be positive.",
        ),
        (
            "check_offer_price",
            "CHECK(price> 0)",
            "Offer price must be positive.",
        ),
    ]

    @api.constrains("selling_price")
    def _validate_selling_price(self):
        for record in self:
            if record.selling_price < 0.9 * record.expected_price:
                raise ValidationError(
                    "Selling price must be at least 90'%' of the expected price"
                )

    @api.constrains("offer_ids")
    def _check_for_offers(self):
        if len(self.offer_ids) > 0:
            self.state = "offer_received"

    @api.ondelete(at_uninstall=False)
    def _unlink_new_properties(self):
        for record in self:
            if record.state != "new" or record.state != "cancelled":
                raise UserError("Property cannot be deleted!")

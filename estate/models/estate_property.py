from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: datetime.now() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        readonly=True,
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
        store=True,
    )
    type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float("Best Price", compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)", "The expected price must be positive"
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price > 0)", "The selling price must be positive"
    )

    _order = "id desc"

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price") or [0])

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = False
            self.garden_orientation = False

    def action_cancel_property(self):
        if self.state == "sold":
            raise UserError("Sold property cannot be cancelled!")

        for record in self:
            record.state = "cancelled"

        return True

    def action_sell_property(self):
        if self.state == "cancelled":
            raise UserError("Cancelled property cannot be sold!")

        for record in self:
            record.state = "sold"

        return True

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if len(record.offer_ids) > 0 and (
                float_compare(record.selling_price, record.expected_price * 0.9, 5)
                == -1
            ):
                raise ValidationError(
                    "The selling price cannot be lower than the 90% of the expected price"
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_except_few_states(self):
        if any(
            (record.state != "new" and record.state != "cancelled") for record in self
        ):
            raise UserError(
                "You cannot remove the property except when the state is new or cancelled!"
            )

    def offer_received(self):
        if self.state == "new":
            self.state = "offer_received"

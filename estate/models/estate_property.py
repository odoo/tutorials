from odoo import api, fields, models
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["mail.thread"]
    _description = "This is the estate property model"
    _order = "id desc"

    name = fields.Char(required=True, tracking=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)
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
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
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
        required=True,
        copy=False,
        default="new",
        tracking=True,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    _sql_constraints = [
        (
            "expected_price_positive",
            "check(expected_price > 0)",
            "Expected Price should be strictly positive.",
        ),
        (
            "selling_price_positive",
            "check(selling_price > 0)",
            "Selling price should strictly be positive",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def set_as_sold(self):
        if self.state == "cancelled":
            raise UserError("Cancelled properties cannot be sold.")
        if "accepted" not in self.offer_ids.mapped("status"):
            raise UserError("Properties with no accepted offer cannot be sold.")
        self.state = "sold"
        self.message_post(
            body=f"The property {self.name} was sold at a price of {self.selling_price}",
            subject="Property Sold",
            message_type="notification",
        )
        return True

    def set_as_cancelled(self):
        if self.state == "sold":
            raise UserError("Sold properties cannot be cancelled.")
        self.state = "cancelled"
        return True

    @api.constrains("selling_price")
    def _selling_price_constraint(self):
        for record in self:
            if (
                float_compare(
                    record.selling_price,
                    0.9 * record.expected_price,
                    precision_digits=2,
                )
                == -1
            ):
                raise ValidationError(
                    "Selling price cannot be lower than 90% of expected price"
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_except_state_new_or_cancelled(self):
        for record in self:
            if record.state != "new" and record.state != "cancelled":
                raise UserError("Only new and cancelled properties can be deleted.")

    def _track_subtype(self, initial_values):
        self.ensure_one()
        if "state" in initial_values and self.state == "sold":
            return self.env.ref("estate.mt_state_change")
        return super()._track_subtype(initial_values)

    def action_set_unsold(self):
        self.write({"state": "offer_received"})

    def _notify_get_recipients_groups(self, message, model_description, msg_vals=None):
        groups = super()._notify_get_recipients_groups(
            message, model_description, msg_vals
        )
        self.ensure_one()
        trip_actions = []
        if self.state == "sold":
            app_action = self._notify_get_action_link(
                "method", method="action_set_unsold"
            )
            trip_actions = [{"url": app_action, "title": "Set Unsold"}]

        new_group = (
            "estate_property_manager",
            lambda pdata: True,
            {"actions": trip_actions, "active": True, "has_button_access": True},
        )
        return [new_group] + groups

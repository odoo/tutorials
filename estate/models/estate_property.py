from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Title", required=True, default="Unknown")
    property_type_id = fields.Many2one("estate.property.type")
    tag_ids = fields.Many2many("estate.property.tag")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3),
    )
    expected_price = fields.Float(required=True, digits=(16, 2))
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [
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
            ("pending_booking", "Pending Booking Payment"),
            ("booked", "Booked"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        copy=False,
        default="new",
        tracking=True,
    )
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        default=lambda self: self.env.user,
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(
        string="Total Area (sqm)", compute="_compute_total_area"
    )
    best_price = fields.Float(compute="_compute_best_price")
    property_maintenance_ids = fields.One2many("property.maintenance", "property_id")
    maintenance_count = fields.Integer(compute="_compute_maintenance_stats")
    has_active_maintenance = fields.Boolean(compute="_compute_maintenance_stats")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property expected price must be strictly positive.",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "A property selling price must be positive."
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = (
                max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0
            )

    @api.depends("property_maintenance_ids.state")
    def _compute_maintenance_stats(self):
        for record in self:
            active_maintenance = record.property_maintenance_ids.filtered(
                lambda m: m.state != "done"
            )
            record.maintenance_count = len(active_maintenance)
            record.has_active_maintenance = record.maintenance_count > 0

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
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
                    _(
                        "The selling price cannot be lower than 90% of the expected price."
                    )
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError(
                    _("You can only delete properties that are 'New' or 'Cancelled'.")
                )

    def action_sold(self):
        self.ensure_one()
        if self.state == "cancelled":
            raise UserError(_("You can not sold a cancelled property."))
        self.state = "sold"
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError(_("You can not cancel a sold property."))
        self.state = "cancelled"
        return True

    def action_best_offer(self):
        self.ensure_one()
        if not self.offer_ids:
            raise UserError(_("There are no offers to accept!"))
        best_offer = max(self.offer_ids, key=lambda o: o.price)
        best_offer.action_accept()
        return True

    def action_view_maintenance(self):
        self.ensure_one()
        return {
            "name": _("Maintenance"),
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "property.maintenance",
            "domain": [("property_id", "=", self.id)],
            "context": {"default_property_id": self.id},
        }

    def action_view_booking(self):
        self.ensure_one()
        booking = self.env["estate.booking"].search(
            [
                ("property_id", "=", self.id),
                ("buyer_id", "=", self.buyer_id.id),
                ("booking_status", "!=", "cancelled"),
            ]
        )

        if not booking:
            booking = self.env["estate.booking"].search(
                [("property_id", "=", self.id)], order="id desc", limit=1
            )

        if not booking:
            raise UserError(_("No booking has been created for this property yet."))

        return {
            "type": "ir.actions.act_window",
            "res_model": "estate.booking",
            "res_id": booking.id,
            "view_mode": "form",
            "target": "current",
        }

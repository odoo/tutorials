from datetime import timedelta

from odoo import _, api, fields, models

from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    description = fields.Text(required=True)
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + timedelta(days=90),
        copy=False,
    )
    expected_price = fields.Float(copy=False)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        readonly=True,
        default='new',
        required=True,
        copy=False,
        tracking=True
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )
    visit_ids = fields.One2many(
        "estate.property.visit",
        "property_id",
        string="visits",
    )
    maintenance_ids = fields.One2many(
        "estate.property.maintenance",
        "property_id",
        string="maintenance requests"
    )
    total_area = fields.Float(
        string="Total Area",
        compute="_compute_total_area"
    )
    best_price = fields.Float(
        string="Best Price",
        compute="_compute_best_price"
    )
    maintenance_count = fields.Integer(
        compute="_compute_request_count"
    )
    visit_count = fields.Integer(
        compute="_compute_visit_count"
    )

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price > 0)",
        "The selling price must be strictly positive",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0.0) + (record.garden_area or 0.0)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue

            minimum_price = record.expected_price * 0.9

            if float_compare(
                record.selling_price,
                minimum_price,
                precision_rounding=0.01,
            ) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
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
    def _unlink_except_new_or_cancelled(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError("Cannot delete a property in this stage")

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled")
            record.state = "cancelled"

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be sold")
            accepted = record.offer_ids.filtered_domain([('status', '=', 'accepted')])
            if not accepted:
                raise UserError("You must accept an offer before selling.")

        template = self.env.ref("estate.email_template_estate")

        ctx = {
            "default_model": "estate.property",
            "default_res_ids": self.ids,
            "default_partner_ids": [self.user_id.partner_id.id, self.buyer_id.id],
            "default_template_id": template.id,
        }

        action = {
            "name": _("Send"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }
        return action

    def _compute_request_count(self):
        for record in self:
            record.maintenance_count = len(record.maintenance_ids)

    def _compute_visit_count(self):
        for record in self:
            record.visit_count = len(record.visit_ids)

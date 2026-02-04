from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from odoo.tools import is_html_empty


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is the table of real estate property data"
    _inherit = ["mail.thread", "mail.activity.mixin"]
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
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        string="State",
        default="new",
        required=True,
        copy=False,
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    customer_id = fields.Many2one(
        "res.partner", string="Customer", copy=False, readonly=True
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        readonly=True,
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tag type")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "check(expected_price > 0)",
        "The Expected Price must be positive",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.model
    def get_empty_list_help(self, help_message):
        if not is_html_empty(help_message):
            return help_message
        help_title = "Create a new property"
        sub_title = "click on new button to create a new property"
        return super().get_empty_list_help(
            f'<p class="o_view_nocontent_smiling_face">{help_title}</p><p class="oe_view_nocontent_alias">{sub_title}</p>'
        )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(
                    _(
                        "The Selling price cannot be lower than 90% of the expected price."
                    )
                )

    @api.constrains("offer_ids")
    def _check_offer_vaild(self):
        if self.filtered(lambda record: record.state == "sold"):
            raise ValidationError(_("Already offer is accept"))
        return True

    @api.ondelete(at_uninstall=False)
    def _check_if_property_state(self):
        if self.filtered(lambda record: record.state not in ("new", "cancelled")):
            raise UserError(
                _("You can only delete properties in new or cancelled state")
            )
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.filtered(lambda record: record.state == "sold"):
            raise UserError(_("You cannot cancel the property that already cancelled"))
        self.write({"state": "cancelled"})

    def action_sold(self):
        self.ensure_one()
        if self.filtered(lambda record: record.state == "cancelled"):
            raise UserError(
                _("You cannot Sold the property offer that already Cancelled")
            )
        if not self.customer_id:
            raise UserError(_("You cannot sold the property that has no customer"))
        self.write({"state": "sold"})
        body = _("Hello, the property <b>%s</b> has been sold for <b>%s</b>.", self.name, self.selling_price)
        ctx = {
            "default_model": "estate.property",
            "default_res_ids": self.ids,
            "default_composition_mode": "comment",
            "default_use_template": False,
            "default_subject": _("Sale Confirmation: %s", self.name),
            "default_body": body,
            "default_partner_ids": [self.customer_id.id] if self.customer_id else [],
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

    def action_best_offer(self):
        self.ensure_one()
        best_offer = self.env["estate.property.offer"].search(
            [("property_id", "=", self.id)], order="price desc", limit=1
        )
        if not best_offer:
            raise UserError(_("Property offer not found first add the offers"))
        best_offer.status = "accepted"
        self.state = "sold"
        self.selling_price = best_offer.price
        other_offer = self.env["estate.property.offer"].search(
            [("property_id", "=", self.id), ("id", "!=", best_offer.id)]
        )
        other_offer.status = "refused"
        self.customer_id = best_offer.partner_id

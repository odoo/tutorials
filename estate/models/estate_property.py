from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError

PROPERTY_STATE = [
    ("new", "New"),
    ("offer_received", "Offer Received"),
    ("accepted", "Offer Accepted"),
    ("sold", "Sold"),
    ("cancelled", "Cancelled"),
]
GARDEN_ORIENTATION = [
    ("north", "North"),
    ("south", "South"),
    ("east", "East"),
    ("west", "West"),
]


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Management Module"
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char(string="Post Code")
    image = fields.Image()
    date_availability = fields.Date(
        string="Availability From",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Monetary(currency_field="currency_id", required=True)
    selling_price = fields.Monetary(
        currency_field="currency_id",
        readonly=True,
        copy=False,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )

    bedrooms = fields.Integer(string="Bed Rooms", default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=GARDEN_ORIENTATION)
    state = fields.Selection(
        string="Status",
        default="new",
        copy=False,
        required=True,
        selection=PROPERTY_STATE,
        tracking=True,
    )
    active = fields.Boolean(default=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Monetary(
        compute="_compute_best_offer",
        currency_field="currency_id",
        store=True,
    )

    _check_positive_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Expected Price Must be in Positive",
    )
    _check_positive_selling_price = models.Constraint(
        "CHECK(selling_price > 0)",
        "Selling Price Must be in Positive",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def onchange_garden(self):
        if self.garden:
            self.garden_area = 1000
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state != "cancelled":
                record.state = "sold"
                record._send_email()
            else:
                raise UserError(
                    _("Property is already cancelled, cannot be marked as sold."),
                )
        return True

    def _send_email(self):
        template = self.env.ref("estate.email_template_property_sold")
        template.send_mail(
            self.id,
            email_layout_xmlid="mail.mail_notification_light",
            email_values={
                "auto_delete": True,
                "email_from": self.env.company.email_formatted,
                "email_to": self._origin.buyer_id.email,
            },
            force_send=True,
        )

    def action_cancel(self):
        if self.state != "sold":
            self.state = "cancelled"
        else:
            raise UserError(_("Property is already sold, cannot be cancelled."))
        return True

    def action_restore(self):
        if self.state == "cancelled":
            self.state = "new"
        else:
            raise UserError(_("Property is not cancelled."))
        return True

    def action_open_offer_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Create Offer Wizard",
            "res_model": "offer.wizard",
            "target": "new",
            "view_mode": "form",
        }

    @api.depends("offer_ids.price")
    def action_accept_best_offer(self):
        max_price_record = self.env["estate.property.offer"].search(
            domain=[("property_id", "in", self.ids)],
            order="price desc",
            limit=1,
        )
        max_price_record.action_accept_offer()

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_is_new_or_cancelled(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError(_("Only new and cancelled properties can be deleted"))

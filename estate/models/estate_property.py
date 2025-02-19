from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    active = fields.Boolean(string="active", default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        store="True",
        compute="_compute_state",
        required=True,
        copy=False,
        group_expand=True,
        tracking=True,
    )
    name = fields.Char(string="Property", tracking=True)
    image_1920 = fields.Image("Image", max_width=1920, max_height=1080)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", tracking=True)
    description = fields.Text(string="Description")
    selling_price = fields.Float(readonly=True, copy=False)
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Availability date",
        default=lambda self: fields.Datetime.today() + timedelta(days=90),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Property Offers"
    )
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive.",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids", "offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        if self.state == "sold":
            raise UserError("A sold property cannot be cancelled.")
        self.state = "cancelled"

    def action_sold(self):
        accepted_offer = self.offer_ids.filtered(lambda o: o.status == "accepted")
        if not accepted_offer:
            raise UserError("Cannot sell a property without an accepted offer.")
        self.state = "sold"
        self.message_post(
            body=f"The property '{self.name}' has been sold for {self.selling_price}!",
            subject="Property Sold",
            message_type="notification",
        )
        template = self.env.ref("estate.mail_template_property_sold")
        template.send_mail(
            self.id, force_send=True, email_layout_xmlid="mail.mail_notification_light"
        )
        message_body = f"Hello {self.partner_id.name}, Congratulations! Your property '{self.name}' has been successfully sold. Thank you!"
        whatsapp_message = self.env[
            "whatsapp.message"
        ].create(
            {
                "body": message_body,
                "mobile_number": self.partner_id.mobile,  # assuming mobile is in international format like +123456789
                "message_type": "outbound",
            }
        )
        whatsapp_message._send()

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        if (
            not float_is_zero(self.selling_price, precision_rounding=0.01)
            and float_compare(
                self.selling_price,
                self.expected_price * 0.9,
                precision_rounding=0.01,
            )
            < 0
        ):
            raise ValidationError(
                "The selling price cannot be lower than 90% of the expected price. Please adjust the selling price or expected price."
            )

    @api.depends("offer_ids.status")
    def _compute_state(self):
        for property in self:
            if not property.offer_ids:
                property.state = "new"
            elif all(offer.status == "refused" for offer in property.offer_ids):
                property.state = "new"
            else:
                property.state = "offer_received"

    @api.ondelete(at_uninstall=False)
    def _prevent_deletion(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(
                    "You can only delete properties in the 'New' or 'Cancelled' state."
                )

    def action_add_offer(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Add Offer",
            "res_model": "estate.property.offer.wizard",
            "view_mode": "form",
            "target": "new",
        }


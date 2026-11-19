from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _inherit = ["mail.thread"]

    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    visit_count = fields.Integer("count", compute="_compute_visitor_count")
    visitor_ids = fields.One2many("estate.visitor", "property_id")

    # def _default_Date(self):
    #     return datetime.now() + relativedelta(months=3)

    property_type_id = fields.Many2one("estate.property.type", "Type")
    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=lambda x: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    salesman_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    active = fields.Boolean(string="Active", default=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        tracking=True,
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price", store=True)

    _check_positive_price = models.Constraint(
        "CHECK (expected_price > 0.0 AND selling_price > 0.0)",
        "price must be strictly positive",
    )

    @api.depends("visitor_ids")
    def _compute_visitor_count(self):
        for visit in self:
            visit.visit_count = len(visit.visitor_ids)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_price = max(rec.offer_ids.mapped("price"))
            else:
                rec.best_price = 0.0

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for property in self:
            if float_is_zero(property.selling_price, precision_rounding=0.01):
                continue

            if (
                float_compare(
                    property.selling_price,
                    property.expected_price * 0.9,
                    precision_rounding=0.01,
                )
                < 0
            ):
                raise ValidationError(
                    self.env._(
                        "Selling price must be at least 90% of the expected price."
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
                    self.env._("Only new and cancelled properties can be deleted.")
                )

    def action_sold(self):
        self.ensure_one()
        accepted_offer = self.offer_ids.filtered(lambda o: o.status == "accepted")
        if not accepted_offer:
            raise UserError(
                self.env._("Cannot set as sold: Please accept an offer first.")
            )

        action = {
            "name": "Send Mail",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "target": "new",
            "context": {
                "default_composition_mode": "comment",
                "default_model": self._name,
                "default_res_ids": self.ids,
                "default_partner_ids": self.buyer_id.ids,
                "default_subject": self.env._("Property sold: %s", self.name),
                "default_body": self.env._(
                    "<p>The property is sold at a selling price of %s.</p>",
                    self.selling_price,
                ),
                "mark_property_sold": True,
            },
        }
        return action

    def message_post(self, **kwargs):
        message = super().message_post(**kwargs)

        if (
            self.env.context.get("mark_property_sold")
            and self.state == "offer_accepted"
        ):
            self.write({"state": "sold"})

        return message

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(
                    self.env._("A sold property cannot set to be cancelled")
                )
            record.state = "cancelled"

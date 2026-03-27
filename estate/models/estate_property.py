from datetime import timedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    active = fields.Boolean(default=True)
    bedrooms = fields.Integer(default=2)
    best_price = fields.Float(
        compute="_compute_best_price",
        string="Best Offer",
        store=True,
        # search="_search_best_price",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.today() + timedelta(days=90)
    )
    description = fields.Text()
    expected_price = fields.Float(required=True)
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
    living_area = fields.Integer()
    maintenance_count = fields.Integer(compute="_compute_maintenance_count")
    maintenance_ids = fields.One2many(
        "estate.property.maintenance", "property_id", string="Maintenance Request"
    )
    name = fields.Char(required=True)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    postcode = fields.Char()
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    selling_price = fields.Float(readonly=True, copy=False)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
        tracking=1
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    total_area = fields.Float(compute="_compute_total_area", store=True)
    visit_ids = fields.One2many("estate.property.visit", "property_id", string="Visits")
    visit_count = fields.Integer(compute="_compute_visit_count")

    _expected_price_check = models.Constraint(
        "CHECK(expected_price > 0)", "The expected price must be strictly positive."
    )
    _selling_price_check = models.Constraint(
        "CHECK(selling_price >= 0)", "The selling price must be positive"
    )

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue

            min_price = record.expected_price * 0.9

            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% the expected price."
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        self.ensure_one()
        if self.state == "cancelled":
            raise UserError(_("A cancelled property cannot be sold."))
        if not self.buyer_id.id:
            raise UserError(_("Buyer is Not selected !!"))
        self.state = "sold"
        self.action_archive()

        ctx = {
            "default_model": "estate.property",
            "default_res_ids": self.ids,
            "default_partner_ids": [
                self.buyer_id.id,
                self.salesperson_id.partner_id.id,
            ],
            "default_template_id": self.env.ref(
                "estate.mail_template_estate_payment_executed"
            ).id,
        }

        action = {
            "name": "Send",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }
        return action

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled.")
            record.state = "cancelled"
        return True

    def action_best_offer(self):
        for record in self:
            if len(record.offer_ids) == 0:
                raise UserError(_("There are no offers to accept for this property."))
            maxi = -1
            for offer in record.offer_ids:
                if offer.price > maxi:
                    max_record = offer
                    maxi = offer.price

            max_record.action_accept()

    @api.depends("maintenance_ids")
    def _compute_maintenance_count(self):
        for record in self:
            record.maintenance_count = len(record.maintenance_ids)

    @api.depends("visit_ids")
    def _compute_visit_count(self):
        for record in self:
            record.visit_count = len(record.visit_ids)

    def _search_best_price(self, operator, value):
        properties = self.search([()])  # get all properties
        matched_ids = []

        for property in properties:
            if (
                (operator == ">" and property.best_price > value)
                or (operator == "<" and property.best_price < value)
                or (operator == "=" and property.best_price == value)
            ):
                matched_ids.append(property.id)

        return [("id", "in", matched_ids)]

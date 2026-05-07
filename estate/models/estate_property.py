from odoo import _, fields, models, api
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    description = fields.Text()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )
    create_property_date = fields.Date()
    postcode = fields.Char(required=True)
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("west", "West"),
            ("south", "South"),
        ],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("accepted", "Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    buyer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Buyer",
        copy=False,
        default=lambda self: self.env.user.partner_id,
    )
    sales_person = fields.Many2one(
        comodel_name="res.users",
        string="Sales person",
        index=True,
        default=lambda self: self.env.user,
    )
    property_tag = fields.Many2many(
        comodel_name="estate.property.tag",
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
    )
    total_area = fields.Integer(
        string="total_area", name="Total area", compute="_compute_total"
    )
    best_price = fields.Integer(
        compute="_compute_best_price",
        store=True,
    )

    @api.model
    def _cron_stale_property(self):
        body_html = self.env.ref("estate.email_template_stale_property_reminder")
        properties = self.search([("state", "=", "new")])
        for i in properties:
            if i.create_property_date:
                time_period = fields.Date.today() - i.create_property_date
                if time_period.days > 30 and i.state == "new":
                    body_html.send_mail(i.id, force_send=True)

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        prices = self.mapped("offer_ids.price")
        self.best_price = max(prices) if prices else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _ondelete_property(self):
        for record in self:
            if record.state != "new" or record.state != "cancelled":
                raise UserError(
                    "You can't delete the record which is not new or cancelled"
                )

    def action_cancel_offer(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Saved properties can't be cancelled")
            else:
                record.state = "cancelled"

    def action_sold_offer(self):
        body_html = self.env.ref("estate.email_for_sold_property")
        for buyer in self:
            if buyer.state == "cancelled":
                raise UserError("Cancelled properties can't be saved")
            else:
                buyer.state = "sold"

            if buyer.buyer_id:
                body_html.send_mail(buyer.id, force_send=True)

        return True

    def action_approve_best(self):
        self.offer_ids[0].status = "accepted"

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0 and selling_price > 0)",
        "Expected price and selling price must be positive",
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_expected_price(self):
        for record in self:
            base = record.expected_price * 0.9
            if record.selling_price and record.selling_price < base:
                raise ValidationError(
                    f"Selling Price must be greater than 90 percent of expected price and atleast {base}"
                )

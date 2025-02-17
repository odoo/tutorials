from datetime import date, timedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["mail.thread", "mail.message.subtype", "mail.activity.mixin"]
    _description = "Real Estate App"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: date.today() + timedelta(days=90)
    )
    expected_price = fields.Float()
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    is_garage = fields.Boolean(string="Garage")
    is_garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_receive", "Offer Received"),
            ("offer_accept", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
        tracking=True,
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type")
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        ondelete="restrict",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", ondelete="restrict", copy=False, tracking=True
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, required=True
    )

    _sql_constraints = [
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling Price of the property should be positive",
        ),
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected Price should be strictly positive",
        ),
    ]

    def _track_subtype(self, init_values):
        self.ensure_one()
        if "status" in init_values and self.status == "offer_receive":
            return self.env.ref("estate.estate_property_offer_receive_state")
        if "status" in init_values and self.status == "offer_accept":
            return self.env.ref("estate.estate_property_offer_accept_state")
        return super(EstateProperty, self)._track_subtype(init_values)

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        # breakpoint() self.env['estate.property'].search([])
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if not record.offer_ids:
                record.best_offer = 0
                continue
            record.best_offer = max(record.offer_ids.mapped("price"))

    @api.onchange("is_garden")
    def _onchange_is_garden(self):
        if self.is_garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains("expected_price", "selling_price")
    def _check_exp_sel_price(self):
        for record in self:
            if (
                record.selling_price < record.expected_price * 0.9
            ) and record.selling_price > 0:
                raise ValidationError(
                    "The selling price must be atleast 90% of expected price"
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_cancel(self):
        for record in self:
            if record.status not in ["new", "cancelled"]:
                raise UserError("Can only delete properties in new or cancelled stage")

    def action_estate_property_sold(self):
        print("Sold button clicked")
        for record in self:
            if record.status == "cancelled":
                raise UserError("Cancelled property can't be sold")
            elif record.status == "sold":
                raise UserError("Property already sold")
            else:
                record.status = "sold"

    def action_estate_property_cancel(self):
        print("Cancel Button Clicked")
        for record in self:
            if record.status == "sold":
                raise UserError("Sold property can't be cancelled")
            elif record.status == "cancelled":
                raise UserError("Property already cancelled")
            else:
                record.status = "cancelled"

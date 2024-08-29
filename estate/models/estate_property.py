from datetime import datetime, timedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        readonly=False,
        default=lambda self: self.env.company,
    )
    property_image = fields.Image("Property Image")
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type", ondelete="cascade"
    )
    salesperson = fields.Many2one(
        "res.users", string="Sales Person", default=lambda self: self.env.user
    )
    buyer = fields.Many2one(
        "res.partner", string="buyer", copy=False, ondelete="cascade"
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    tag_ids = fields.Many2many(
        "estate.property.tag", string="Tags ID", ondelete="cascade"
    )
    postcode = fields.Char()
    description = fields.Text()
    availability_date = fields.Date(
        default=lambda self: datetime.today() + timedelta(days=90), copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(default=10000, readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("canceled", "Canceled"),
            ("sold", "Sold"),
        ],
        required=True,
        copy=False,
        default="new",
        string="Status",
        tracking=True,
    )
    total_area = fields.Float(compute="_compute_total")
    best_offer = fields.Float(compute="_compute_price")
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be strictly positive",
        )
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_price(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped("price"))
            else:
                record.best_offer = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.ondelete(at_uninstall=True)
    def unable_delete_on_state(self):
        if any(user.state in ("new", "canceled") for user in self):
            raise UserError("Can't delete an active user!")

    @api.constrains("selling_price", "expected_price")
    def _check_selling(self):
        for record in self:
            if record.selling_price < 0.9 * record.expected_price:
                raise ValidationError(
                    "You can not make offer if the price is much lower"
                )

    def action_set_sold(self):
        print("sold is clicked")
        for record in self:
            if record.state == "canceled":
                raise UserError("You can not change status to sold if it is canceled")
            else:
                record.state = "sold"

    def action_set_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("You can not change status to canceled if it is sold")
            else:
                record.state = "canceled"
        return True

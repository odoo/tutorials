from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo import fields, api, models


class estate_property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "sequence, id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    description = fields.Text()
    sequence = fields.Integer("Sequence")
    postcode = fields.Char()
    date_availability = fields.Date(default=date.today() + relativedelta(month=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    livingArea = fields.Integer()
    garage = fields.Integer()
    facades = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        default="new",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        tracking=True,
    )
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    property_type = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one(
        "res.users", string="Selesperson", default=lambda self: self.env.user.partner_id
    )
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", copy=False, ondelete="cascade"
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total")
    best_offer = fields.Float(compute="_best_offer")
    _sql_constraints = [
        (
            "check_Expected_price",
            "CHECK(expected_price > 0)",
            "Expected Price must be strictly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling Price selling price must be positive",
        ),
        ("unique_name", "UNIQUE(name)", "Property type name must be unique"),
    ]

    @api.depends()
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.livingArea

    @api.depends("offer_ids")
    def _best_offer(self):
        maximum_price = 0
        for record in self.offer_ids:
            if record.price > maximum_price:
                maximum_price = record.price
        self.best_offer = maximum_price

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 0.00

    def button_action_sold(self):
        if self.state == "canceled":
            raise UserError("Can't be Sold")
        else:
            self.state = "sold"

    def button_action_cancled(self):
        if self.state == "sold":
            raise UserError("Can't be Cancle, It is already Sold")
        else:
            self.state = "canceled"

    @api.constrains("selling_price", "expected_price")
    def _price_constrains(self):
        for record in self:
            if record.selling_price > 0:
                if record.selling_price < 0.9 * record.expected_price:
                    raise ValidationError(
                        "Selling price cannot be lower than 90% of the expected price"
                    )
                else:
                    pass

    @api.ondelete(at_uninstall=False)
    def _delete_state(self):
        for record in self:
            if record.state != "new" and record.state != "canceled":
                raise ValidationError("can't be deleted")

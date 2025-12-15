from dateutil.relativedelta import relativedelta

from odoo import models, api, fields, exceptions
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqft)")
    garden_orientation = fields.Selection([
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West"),
    ])
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="new",
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", required=True)
    customer = fields.Many2one("res.partner", string="Customer", copy=False)
    salesperson = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Integer(compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)", "Expected price must be strictly positive."
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "Selling price must be positive."
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if not record.mapped("offer_ids.price"):
                record.best_price = 0
            else:
                record.best_price = max(record.mapped("offer_ids.price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold_property(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError("Properties which are Cancelled cannot be Sold")
            else:
                record.state = "sold"
        return True

    def action_cancel_offer(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("Properties which are Sold cannot be Cancelled")
            else:
                record.state = "cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_percentage_criteria(self):
        for record in self:
            selling_price_percentage = (record.selling_price / record.expected_price) * 100
            if selling_price_percentage >= 90 or selling_price_percentage == 0:
                pass
            else:
                raise ValidationError(
                    "The selling price cannot be lower then 90% of the expected price."
                )

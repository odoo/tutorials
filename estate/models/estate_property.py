from odoo import api, fields, models, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "Real estate property"

    rounding = 0.01

    name = fields.Char("Property Name", required=True)
    description = fields.Text()
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )

    postcode = fields.Char(required=True)
    date_availability = fields.Date(
        "Availability date",
        copy=False,
        default=fields.Datetime.add(fields.Datetime.today(), months=3),
    )
    expected_price = fields.Float("Expected price", required=True)
    selling_price = fields.Float("Selling price", readonly=True, copy=False, default=0)
    bedrooms = fields.Integer("Number of bedrooms", required=True, default=2)
    living_area = fields.Integer("Living area (sqm)", required=True)
    facades = fields.Integer("Number of facades", required=True)
    garage = fields.Boolean("Has a garage", required=True)
    garden = fields.Boolean("Has a garden", required=True)
    garden_area = fields.Integer("Garden (sqm)")
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[
            ("north", "North"),
            ("west", "West"),
            ("east", "East"),
            ("south", "South"),
        ],
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")

    total_area = fields.Float("Total area (sqm)", compute="_compute_total_area")

    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_offer = fields.Float("Best Offer", compute="_compute_best_offer")

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK (expected_price > 0)",
            "The expected price should be positive.",
        ),
        (
            "check_selling_price",
            "CHECK (selling_price > 0 OR NOT (state = 'sold'))",
            "The selling price should be positive if property is sold.",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = (
                0
                if len(record.offer_ids) == 0
                else max(record.mapped("offer_ids.price"))
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            if self.garden_area == 0:
                self.garden_area = 10
            if self.garden_orientation == False:
                self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.onchange("garden_area")
    def _onchange_garden_area(self):
        if self.garden_area <= 0:
            self.garden_area = 0
            self.garden = False
            self.garden_orientation = False
        else:
            self.garden = True
            if self.garden_orientation == False:
                self.garden_orientation = "north"

    def action_set_sold(self):
        flag = False
        for record in self:
            if record.state != "cancelled":
                record.state = "sold"
            else:
                flag = True
        if flag:
            raise UserError("Cancelled properties can't be sold.")
        return True

    def action_cancel(self):
        flag = False
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            else:
                flag = True
        if flag:
            raise UserError("Sold properties can't be cancelled.")
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=self.rounding):
                continue
            if (
                float_compare(
                    record.selling_price,
                    0.9 * record.expected_price,
                    precision_rounding=self.rounding,
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price cannot be less than 90% than the expected price."
                )

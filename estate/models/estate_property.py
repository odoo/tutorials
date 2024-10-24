from odoo import api, exceptions, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta


class Estate_Property(models.Model):
    _name = "estate_property"
    _description = "Estate properties"
    active = False

    name = fields.Char(required=True, string="Title")

    status = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        readonly=True,
        copy=False,
        string="Sale State",
    )

    description = fields.Text(copy=False, string="Description")

    postcode = fields.Char(
        help="Une adresse serait mieux mais bon...", string="Postcode"
    )

    date_availability = fields.Date(
        default=(date.today() + relativedelta(months=+3)),
        copy=False,
        string="Available From",
    )

    expected_price = fields.Float(
        default=0.0, required=True, copy=False, string="Expected Price"
    )

    selling_price = fields.Float(readonly=True, string="Selling Price")

    bedrooms = fields.Integer(default=2, string="Bedrooms")

    living_area = fields.Integer(string="Living Area (sqm)")

    facades = fields.Integer(default=2, string="Facades")

    garage = fields.Boolean(default=False, string="Garage")

    garden = fields.Boolean(default=False, string="Garden")

    garden_area = fields.Integer(default=0, string="Garden Area (sqm)")

    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("west", "West"), ("east", "East")],
        string="Garden Orientation"
    )

    property_type = fields.Many2one("estate_property_type", string="Property Type")

    buyer = fields.Many2one("res.partner", copy=False, string="Buyer")

    salesperson = fields.Many2one(
        "res.users", default=(lambda self: self.env.user), string="Salesman"
    )

    tag_ids = fields.Many2many("estate_property_tag", string="Property Tags")

    offer_ids = fields.One2many("estate_property_offer", "property_id", string="Offers")

    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")

    best_offer = fields.Float(compute="_compute_best_offer", default=0.0, string="Best Offer")

    _sql_constraints = [
        ("check_positive_expected_price", "CHECK(expected_price >= 0.0)", "Expected Price should be a positive number."), ("check_positive_selling_price", "CHECK(selling_price >= 0.0)", "Selling Price should be a positive number.")
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.constrains("selling_price", "expected_price")
    def _check_expected_vs_selling_price(self):
        for record in self:
            if (record.selling_price > 0.0) and (record.selling_price < 0.9 * record.expected_price):
                raise exceptions.ValidationError(r"Cannot sell for less than 90% of expected price.")

    def action_sold(self):
        for record in self:
            if record.status != "canceled":
                record.status = "sold"
            else:
                raise exceptions.UserError("Canceled properties cannot be sold.")
        return True

    def action_cancel(self):
        for record in self:
            if record.status != "sold":
                record.status = "canceled"
            else:
                raise exceptions.UserError("Sold properties cannot be canceled.")
        return True

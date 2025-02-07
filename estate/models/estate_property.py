# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Properties/Advertisements created and managed in estate"
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

    name = fields.Char(string="Name of the property", required=True)
    description = fields.Text(string="Property Description")
    postcode = fields.Char(string="Postal code")
    date_availability = fields.Date(
        "Availability From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Float(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    total_area = fields.Float(compute="_compute_total_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_recieved", "Offer Recieved"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Offer Status",
        default="new",
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
        required=True,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    best_price = fields.Float(
        compute="_compute_best_price", string="Best Offer", store=True
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onChange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled property cannot be sold")
            if not record.buyer_id or not record.selling_price:
                raise UserError(
                    "Property must have an accepted offer before being sold"
                )
            record.state = "sold"

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold Property can't be canceled")
            record.state = "canceled"

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if (
                record.selling_price > 0
                and record.selling_price < record.expected_price * 0.9
            ):
                raise ValidationError(
                    "The selling price cannot be less than 90% of the expected price"
                )

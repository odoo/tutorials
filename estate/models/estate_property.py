# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="this is used to indicated the garden orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        help="indicates the state of the property ad",
    )
    estate_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Sales Person")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total")

    _check_expected_price_positive = models.Constraint(
        "CHECK(expected_price >= 0)", "The expected price must be positive."
    )
    _check_selling_price_positive = models.Constraint(
        "CHECK(selling_price >= 0)", "The selling price must be positive."
    )

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = None

    def cancel_sale(self):
        for record in self:
            record.state = "cancelled"

    def mark_as_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise ValidationError("Cancelled properties cannot be sold.")
            record.state = "sold"

    @api.constrains("selling_price", "expected_price")
    def _check_date_end(self):
        for record in self:
            if any(
                float_is_zero(value, precision_digits=2) 
                for value in (record.selling_price, record.expected_price)
            ):
                raise ValidationError(
                    "Selling price and expected price must be greater than zero."
                )
            if float_compare(
                record.selling_price, 
                record.expected_price * 0.9, 
                precision_digits=2
            ) < 0:
                raise ValidationError(
                    "Selling price cannot be lower than 90%of expected price!"
                )

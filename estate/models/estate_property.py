from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from datetime import timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive.",
    )

    name = fields.Char('Name', required=True, default='My new house')
    description = fields.Text('Description')
    active = fields.Boolean(default=True)
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', default=lambda self: fields.Date.context_today(self) + timedelta(days=90), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('#Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')

    garden_orientation = fields.Selection([
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West"),
    ])

    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type"
    )

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
    )

    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user
    )

    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags"
    )

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )

    total_area = fields.Float(
        compute="_compute_total_area",
        string="Total Area",
    )

    best_price = fields.Float(
        compute="_compute_best_price",
        string="Best Offer",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (
                    record.create_date.date() + timedelta(days=record.validity)
            )
            else:
                record.date_deadline = fields.Date.context_today(self)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled.")
            record.state = "cancelled"
        return True

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be sold.")
            record.state = "sold"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue

            min_price = record.expected_price * 0.9

            if float_compare(
                record.selling_price,
                min_price,
                precision_rounding=0.01
            ) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

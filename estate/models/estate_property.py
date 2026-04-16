from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = " Real estate Property"
    _order = "id desc"

    name = fields.Char(required=True, default="UNKNOWN")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        compute="_compute_state",
        default='new',
        copy=False,
        required=True,
        store=True
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="property type",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
    )
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tags_ids = fields.Many2many(
        "estate.property.tag",
        string="tags",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
    )
    issue_ids = fields.One2many(
        "estate.property.issue",
        "property_id"
    )
    visit_ids = fields.One2many("estate.property.visit", "property_id")
    visit_count = fields.Integer(compute="_compute_visit_count")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'A property expected price must be strictly positive'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)',
        'A property selling price must be positive'
    )

    @api.depends("offer_ids")
    def _compute_state(self):
        for record in self:
            if record.offer_ids:
                record.state = "offer_received"
            else:
                record.state = "new"

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0

    def _compute_visit_count(self):
        for record in self:
            record.visit_count = len(record.visit_ids)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:

            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            min_price = record.expected_price * 0.9

            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(
                    "Selling price cannot be lower than 90% of expected price.")

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_("Cancelled property can not be sold"))

            if record.issue_ids.priority == 'high' and record.issue_ids.state != 'resolved':
                raise UserError(_("you can not sold overdue property"))

            if not any(o.status == 'accepted' for o in record.offer_ids):
                raise UserError(_("Accept an offer first"))
            else:
                record.state = 'sold'

    def action_cancle(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Sold property can not be Cancelled"))

            record.state = 'cancelled'

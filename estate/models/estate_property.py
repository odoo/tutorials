import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property model"
    _order = "id desc"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=datetime.date.today() + relativedelta(months=3), string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        default="new",
        copy=False,
        string="status",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    _check_expected_price_positive = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property cannot be negative',
    )

    _check_selling_price_positive = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price of a property cannot be negative',
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_to_expected_price_ratio(self):
        for record in self:
            if float_compare(record.selling_price, 0.9 * record.expected_price, 2) == -1 and not float_is_zero(record.selling_price, 2):
                raise ValidationError("Selling price cannot be less than 90% of expected price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else None

    def action_mark_as_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("A Cancelled property cannot be sold")
            else:
                record.state = 'sold'
        return True

    def action_mark_as_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be cancelled")
            else:
                record.state = 'cancelled'
        return True

    @api.ondelete(at_uninstall=False)
    def prevent_deletion_if_not_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("Only New or Cancelled properties can be deleted")

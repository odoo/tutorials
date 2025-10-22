from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare

from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    _check_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'A property expected price must be strictly positive',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)',
        'A property selling price must be positive',
    )

    name = fields.Char('Property Name', required=True)
    description = fields.Text()
    type_id = fields.Many2one('estate.property.type', 'Property Type')
    notes = fields.Html()
    active = fields.Boolean(default=True)

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    date_available = fields.Datetime(
        "Available From",
        copy=False,
        default=date.today() + relativedelta(months=3),
    )
    postcode = fields.Char()
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute='_compute_best_price', readonly=True)
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    living_area = fields.Integer("Living Area (sqm)")
    garden_area = fields.Integer()
    total_area = fields.Float(compute="_compute_total_area", readonly=True)
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
    )
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        default='new',
        copy=False
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price == 0:
                return
            if float_compare(record.selling_price, record.expected_price * 0.9, 1) < 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'south'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sell(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("A cancelled property cannot be sold")
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be cancelled")
            record.state = 'cancelled'
        return True

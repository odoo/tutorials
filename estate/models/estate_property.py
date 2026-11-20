from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.orm.utils import ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    name = fields.Char('Property Name', required=True, default="Unknown")
    description = fields.Text()
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user
    )
    postcode = fields.Char()

    def _default_date_availability(self):
        return fields.Date.context_today(
            self,
            timestamp=fields.Datetime.now() + timedelta(weeks=3 * 4),
        )

    date_availability = fields.Date(
        'Available From',
        default=_default_date_availability,
        copy=False,
    )
    expected_price = fields.Float(required=True)
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'
    )
    selling_price = fields.Float(readonly=True, copy=False)
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)', 'The selling price must be positive.'
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        default='new',
    )
    last_seen = fields.Datetime(default=fields.Datetime.now)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(string='Best Price', compute='_compute_best_price')

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be canceled.')
            record.state = 'canceled'
            return True

    def action_sold_property(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Canceled properties cannot be sold.')
            record.state = 'sold'
            return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_minimum(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            minimum_price = record.expected_price * 0.9
            if (
                float_compare(record.selling_price, minimum_price, precision_digits=2)
                < 0
            ):
                raise ValidationError(
                    'The selling price must be greater than or equal to 90% of the expected price.'
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_new_or_canceled(self):
        for record in self:
            if any(record.state not in ('new', 'canceled') for record in self):
                raise UserError('Only new or canceled properties can be deleted.')

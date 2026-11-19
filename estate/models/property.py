from typing import cast

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import date_utils, float_utils


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Property'

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        'Available From',
        copy=False,
        default=lambda _: date_utils.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        default='new',
    )
    active = fields.Boolean('Active', default=True)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
    )
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesman',
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
    )
    total_area = fields.Integer(
        'Total Area (sqm)',
        compute='_compute_total_area',
    )
    best_price = fields.Float('Best Offer', compute='_compute_best_price')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property must be strictly positive.',
    )
    _check_selling_price_positive = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price of a property must be positive.',
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self) -> None:
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self) -> None:
        for record in self:
            offer_prices = cast(
                'list[int]',
                record.offer_ids.mapped('price'),
            )
            record.best_price = max(offer_prices) if offer_prices else 0

    @api.constrains('selling_price')
    def _check_selling_price_against_expected_price(self) -> None:
        for record in self:
            if (
                not float_utils.float_is_zero(
                    record.selling_price,
                    precision_rounding=.01,
                )
                and float_utils.float_compare(
                    record.selling_price,
                    record.expected_price * .90,
                    precision_rounding=.01,
                ) == -1
            ):
                raise ValidationError(
                    'The selling price must be at least 90% of the expected '
                    'price! You must reduce the expected price if you want to '
                    'accept this offer.'
                )

    @api.onchange('garden')
    def _onchange_garden(self) -> None:
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self) -> bool:
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Cannot sell a cancelled property.')

            record.state = 'sold'

        return True

    def action_cancel(self) -> bool:
        for record in self:
            if record.state == 'sold':
                raise UserError('Cannot cancel a sold property.')

            record.state = 'cancelled'

        return True

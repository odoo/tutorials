# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import date_utils
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate property"
    _order = "id desc"

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive.',
    )

    name = fields.Char('Estate Name', required=True)
    description = fields.Text('Estate Description')
    postcode = fields.Char('Zip code')
    date_availability = fields.Date('Availability date', default=lambda self: fields.Date.add(
        fields.Date.today(), months=3))
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Number of bedrooms', default=2)
    living_area = fields.Integer('Living area (sqm)')
    facades = fields.Integer('Number of facades')
    garage = fields.Boolean('Has a garage')
    garden = fields.Boolean('Has a garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new',
        copy=False,
        required=True
    )
    property_type_id = fields.Many2one(
        'estate.property.type', string="Property Type")
    buyer = fields.Many2one(
        'res.partner', string='Buyer', index=True, copy=False)
    seller = fields.Many2one(
        'res.users', string='Salesman', index=True, default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Integer(
        "Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float('Best price', compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(r.price for r in record.offer_ids)
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 10
        self.garden_orientation = 'north'

    def action_sold(self):
        for property in self:
            if property.state == "canceled":
                raise UserError("Un bien annulé ne peut pas être vendu.")
            property.state = "sold"
        return True

    def action_cancel(self):
        for property in self:
            if property.state == "sold":
                raise UserError("Un bien vendu ne peut pas être annulé.")
            property.state = "cancelled"
        return True

    # @api.constrains('product_id')
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            if (
                float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_rounding=0.01,
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    "You must reduce the expected price if you want to accept this offer."
                )

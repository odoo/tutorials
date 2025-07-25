from odoo import exceptions, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char('Property Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        'Available from',
        default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3),
        copy=False
    )
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean('Active', default=True)
    status = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', "Cancelled")
        ],
        default='new'
    )
    # Many to one relation with property type model
    property_type_id = fields.Many2one('estate.property.type', string='Property type')
    # Customer
    partner_id = fields.Many2one('res.partner', string='Buyer', index=True)
    # Internal User
    user_id = fields.Many2one('res.users', string='Salesman', index=True, default=lambda self: self.env.user)
    # Many to many relation with Tags model
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tag')
    # One to many relation with offer model
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    # Total area as computed field
    total_area = fields.Float(compute='_compute_total_area')
    # Best Price as computed field
    best_price = fields.Float(compute='_compute_best_price')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price should be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price should be positive')
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            # Skip the check if selling_price is zero
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue

            # Compare selling_price with 90% of expected_price
            min_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_price, precision_rounding=0.01) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price') or [0.0])

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # Method to set property sold
    def action_set_sold(self):
        for record in self:
            if record.status == 'cancelled':
                raise exceptions.UserError("A cancelled property cannot be marked as sold.")
            record.status = 'sold'
        return True

    # Method to cancel the property
    def action_set_cancel(self):
        for record in self:
            if record.status == 'sold':
                raise exceptions.UserError("A sold property cannot be cancelled.")
            record.status = 'cancelled'
        return True

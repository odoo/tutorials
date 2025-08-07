# Python Imports
from datetime import date
from dateutil.relativedelta import relativedelta

# Odoo Imports
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    # -----------------------------
    # SQL Constraints
    # -----------------------------
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price cannot be negative.')
    ]

    # -----------------------------
    # Field Declarations
    # -----------------------------
    name = fields.Char(string='Title', required=True, help='Title or name of the property.')
    description = fields.Text(string='Description', help='Detailed description of the property.')
    postcode = fields.Char(string='Postcode', help='Postal code of the property location.')
    date_availability = fields.Date(
        string='Availability From',
        copy=False,
        default=(date.today() + relativedelta(months=3)),
        help='Date from which the property will be available.'
    )
    expected_price = fields.Float(string='Expected Price', required=True, help='Price expected by the seller for this property.')
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False, help='Final selling price once the property is sold.')
    bedrooms = fields.Integer(string='Bedrooms', default=2, help='Number of bedrooms in the property.')
    living_area = fields.Integer(string='Living Area (sqm)', help='Living area size in square meters.')
    facades = fields.Integer(string='Facades', help='Number of facades of the property.')
    garage = fields.Integer(string='Garage', help='Number of garage spaces.')
    garden = fields.Boolean(string='Garden', help='Whether the property has a garden.')
    garden_area = fields.Integer(string='Garden Area (sqm)', help='Size of the garden area in square meters.')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        default='north', help='Direction the garden faces.'
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
        required=True, copy=False, default='new', help='Current status of the property.'
    )
    active = fields.Boolean(string='Active', default=True, help='Whether the property is active and visible.')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', help='Type or category of the property.')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False, help='Partner who bought the property.')
    sales_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user, help='Salesperson responsible for the property.')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags', help='Tags to classify the property.')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers', help='Offers made on this property.')

    # -----------------------------
    # Computed Fields
    # -----------------------------
    total = fields.Float(
        string='Total (sqm)',
        compute='_compute_total_area',
        help='Total area of the property including living and garden areas.'
    )
    best_price = fields.Float(
        string='Best Offer',
        compute='_compute_best_price',
        help='Highest offer price received for the property.'
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        """Compute total area as sum of living area and garden area."""
        for record in self:
            record.total = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        """Compute highest offer price or 0 if no offers."""
        for record in self:
            offer_prices = record.offer_ids.mapped('price')
            record.best_price = max(offer_prices) if offer_prices else 0.0

    # -----------------------------
    # Action Methods
    # -----------------------------
    def action_sold(self):
        """Set property state to 'sold', with validation against invalid states."""
        if not self.offer_ids:
            raise UserError('No offer available for this property.')
            return

        for record in self:
            if record.state == 'cancelled':
                raise UserError('A cancelled property cannot be set as sold.')
            elif record.state == 'sold':
                raise UserError('Property is already sold.')
            else:
                record.state = 'sold'

    def action_cancel(self):
        """Set property state to 'cancelled', with validation against invalid states."""
        if not self.offer_ids:
            raise UserError('No offer available for this property.')
            return

        for record in self:
            if record.state == 'sold':
                raise UserError('A sold property cannot be cancelled.')
            elif record.state == 'cancelled':
                raise UserError('Property is already cancelled.')
            else:
                record.state = 'cancelled'

    # -----------------------------
    # Constraints
    # -----------------------------
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_above_90_percent(self):
        """
        Validate selling price with float precision.
        Ignores zero selling price, otherwise enforces minimum 90% threshold.
        """
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_acceptable_price = 0.9 * record.expected_price
            if float_compare(record.selling_price, min_acceptable_price, precision_digits=2) < 0:
                raise ValidationError(_(
                    "The selling price must be at least 90%% of the expected price.\n"
                    "Expected Price: %(expected_price).2f\nSelling Price: %(selling_price).2f",
                    {
                        'expected_price': record.expected_price,
                        'selling_price': record.selling_price
                    }
                ))

    @api.ondelete(at_uninstall=False)
    def _check_can_be_deleted(self):
        """
        Restrict deletion to properties in 'new' or 'cancelled' state.
        Raises UserError otherwise.
        """
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError('You can only delete properties that are New or Cancelled.')

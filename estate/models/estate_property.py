"""Model of an estate property."""

import datetime

from odoo import api, fields, models

from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    """Estate Property model."""

    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char('Name', required=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', required=True)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    best_offer = fields.Float('Best Offer', readonly=True, compute='_compute_best_offer')
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date', copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
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
            ('west', 'West'),
            ('south', 'South'),
            ('east', 'East'),
        ]
    )
    total_area = fields.Integer('Total Area', compute='_compute_total_area', readonly=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
    )

    active = fields.Boolean('Active', default=True)

    _sql_constraints = [
        ('selling_price', 'CHECK(selling_price > 0)', 'Prices must be strictly positive.'),
        ('expected_price', 'CHECK(expected_price > 0)', 'Prices must be strictly positive.'),
    ]

    _order = "id desc"

    def action_set_cancelled(self):
        """Cancel a property."""
        for estate in self:
            if estate.state == 'sold':
                raise UserError('Sold properties can not be cancelled')
            else:
                estate.state = 'cancelled'
        
        return True

    def action_set_sold(self):
        """Sell a property."""
        for estate in self:
            if estate.state == 'cancelled':
                raise UserError('Cancelled properties can not be sold')
            else:
                estate.state = 'sold'
        
        return True
    
    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        """Compute total area from garden area and living area."""
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        """Compute best offer from all linked offers."""
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0.0)
    
    @api.onchange("garden")
    def _onchange_garden(self):
        """Update garden related fields on garden enabling/disabling."""
        for estate in self:
            if self.garden:
                self.garden_area = 10
                self.garden_orientation = 'north'
            else:
                self.garden_area = 0
                self.garden_orientation = ''
    
    @api.constrains('selling_price')
    def _check_selling_price(self):
        """Constrains the selling price to be at least 80% of the expected price."""
        for estate in self:
            if estate.state == 'offer_accepted' and float_compare(estate.selling_price, estate.expected_price*0.8, precision_rounding=0.01) == -1:
                raise ValidationError('Selling price must be at least 80% of the expected price.')
    
    @api.ondelete(at_uninstall=False)
    def _unlink_only_new_cancelled(self):
        """Avoids deletion of a property if it's not new or cancelled."""
        if any(estate.state not in ['new', 'cancelled'] for estate in self):
            raise UserError("Can't delete a property if it's not new or cancelled")


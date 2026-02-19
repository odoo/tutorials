# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties"
    _order = "id desc"

    name = fields.Char('Property Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
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
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Type is used to choose the orientation")
    property_type_id = fields.Many2one('estate.property.type', string='Property Types')
    seller_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True, copy=False, default='new')
    total_area = fields.Integer('Total Area (sqm)', compute="_compute_total_area")
    best_price = fields.Float('Best Offer', compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.garden_area + line.living_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for line in self:
            if line.offer_ids:
                line.best_price = max(line.offer_ids.mapped('price'))
            else:
                line.best_price = 0.0

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                error_msg = "You cannot sell a canceled property."
                raise UserError(error_msg)
        return True

    def action_cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                error_msg = "You cannot cancel a sold property."
                raise UserError(error_msg)
        return True

    _check_positive_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property should be strictly positive.',
    )

    _check_positive_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price of a property should be positive or zero.',
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_price_offer(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            expected_price = record.expected_price
            selling_price = record.selling_price
            if float_compare(selling_price, expected_price * 0.9, precision_digits=2) < 0:
                error_msg = "The selling price should be at least 90% of the expected price."
                raise ValidationError(error_msg)

    @api.ondelete(at_uninstall=False)
    def _unlink_check_state(self):
        for record in self:
            if record.state != 'new' and record.state != 'canceled':
                error_msg = "Only properties in 'New' or 'Canceled' status can be deleted."
                raise UserError(error_msg)

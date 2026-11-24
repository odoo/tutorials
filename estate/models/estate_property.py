from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A Free Real Estate Property"
    _order = "id desc"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text('Description', translate=True)

    salesman_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', required=True)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    postcode = fields.Char('Postcode', required=False, translate=True)
    date_availability = fields.Datetime('Availability date', required=False, copy=False, default=fields.Datetime.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', digits=(10, 3), required=True)
    selling_price = fields.Float('Selling Price', digits=(10, 3), required=False, readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', required=False, default=2)
    living_area = fields.Integer('Living area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Determines garden's orientation")
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], required=True, copy=False, default='new')
    active = fields.Boolean(string='Active', default=True)

    total_area = fields.Float('Total Area (sqm)', compute='_sum_total_area')
    best_price = fields.Float('Best Offer', compute='_compute_best_price')

    _positive_expected_price = models.Constraint('CHECK(expected_price > 0)', 'Expected price must be strictly positive.')
    _positive_selling_price = models.Constraint('CHECK(selling_price >= 0)', 'Selling price must be positive.')

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._('Cancelled property cannot be sold.'))
            if not record.buyer_id:
                raise UserError(self.env._('You cannot sell a property that has no buyer.'))
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._('You cannot cancel a sold property.'))
            record.state = 'cancelled'
        return True

    @api.depends("living_area", "garden_area")
    def _sum_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=3) or float_is_zero(record.expected_price, precision_digits=3):
                continue
            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=3) < 0:
                raise UserError(self.env._('The selling price cannot be lower than 90% of the expected price.'))

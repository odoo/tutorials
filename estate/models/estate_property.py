from odoo import api, models, fields
from odoo.exceptions import UserError
import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "test description"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date availability', copy=False, default=datetime.date.today() + relativedelta(months=+3))
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area (sqm)')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='state',
        selection=[('new', 'New'), ('offerreceived', 'Offer Received'), ('offeraccepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new',
    )
    total_area = fields.Integer('Total area (sqm)', compute='_compute_total_area')
    best_offer = fields.Float('Best price', compute='_compute_best_offer')
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_set_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('A sold property cannot be cancelled')
            else:
                record.state = 'cancelled'
        return True

    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('A cancelled property cannot be sold')
            else:
                record.state = 'sold'
        return True

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be striclty positive',
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive',
    )

    @api.constrains('selling_price')
    def check_selling_price(self):
        for record in self:
            expected_minimum = record.expected_price * 0.9
            if float_compare(record.selling_price, expected_minimum, precision_digits=2) < 0:
                raise UserError(r'The selling price should be at least 90% of the expexted price')

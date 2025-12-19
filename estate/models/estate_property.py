from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _
from datetime import timedelta


def default_availability_date(recordset):
    return fields.Date.context_today(recordset) + timedelta(days=90)


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Advertisement module"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date availability', copy=False, default=default_availability_date)
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden orientation')
    total_area = fields.Integer('Total Area', compute='_compute_total_area')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], string="State", default='new', required=True, copy=False)
    property_type_id = fields.Many2one('estate.property.type', string="Property type")
    property_buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    property_salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string="Property tags")
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers', inverse='_inverse_offers')
    best_price = fields.Float('Best Price', compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('property_offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            offer_prices = record.property_offer_ids.mapped('price')
            record.best_price = max(offer_prices) if offer_prices else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def _inverse_offers(self):
        for record in self:
            if record.state == 'new' and record.property_offer_ids:
                record.state = 'offer_received'

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_('Cancelled properties cannot be sold.'))
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('Sold properties cannot be cancelled.'))
            record.state = 'cancelled'
        return True

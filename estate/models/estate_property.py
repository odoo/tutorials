# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.today()+relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True) # testing the reserved fields thing
    state = fields.Selection(selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
                            default='new',
                            required=True,
                            copy=False
                        )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    seller_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property must be strictly positive!'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price of a property must be strictly positive!'
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_price(self):
        for record in self:
            if float_is_zero(record.selling_price, 3):
                continue
            if float_compare(record.selling_price, 0.9*record.expected_price, 3) == -1:
                raise exceptions.ValidationError("The selling price cannot be less than 90% of the expected price")
    

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area+record.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0

    @api.onchange('offer_ids')
    def _onchange_receive_offer(self):
        for record in self.filtered(lambda record: record.state == 'new'):
            if record.offer_ids:
                record.state = 'offer received'
                

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False

    def action_mark_as_sold(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise exceptions.UserError("Canceled properties cannot be sold!")
    
    def action_mark_as_canceled(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise exceptions.UserError("Sold properties cannot be canceled!")

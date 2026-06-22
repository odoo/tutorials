from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class AwesomeEstateProperty(models.Model):
    _name = 'awesome.estate.property'
    _description = "Real Estate Property"
    _rec_name = 'name'
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    property_type_id = fields.Many2one(
        'awesome.estate.property.type', 
        ondelete='restrict',)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many('awesome.estate.property.tag')
    offer_ids = fields.One2many(
        'awesome.estate.property.offer',
        'property_id',
        string="Offers",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default='new',
    )
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )
    total_area = fields.Integer(compute='_compute_total_area', store=True)
    squared_area = fields.Integer(compute='_compute_squared_area', store=True)

    best_price = fields.Float(compute='_compute_best_price', store=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('living_area', 'garden_area', 'total_area')
    def _compute_squared_area(self):
        for record in self:
            record.squared_area = record.total_area ** 2

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(
                record.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        self.ensure_one()
        if self.state == 'cancelled':
            raise UserError("Cancelled properties cannot be sold.")
        self.state = 'sold'
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'sold':
            raise UserError("Sold properties cannot be cancelled.")
        self.state = 'cancelled'
        return True

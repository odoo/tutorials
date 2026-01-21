from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.context_today(self) + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new',
    )
    active = fields.Boolean(default=True)

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')

    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)

    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)

    tag_ids = fields.Many2many('estate.property.tag', string='Property Tag')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    total_area = fields.Integer(compute='_compute_total_area')

    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('garden_area', 'total_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices, default=0.0)
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('A canceled property cannot be set as sold.')
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('A sold property cannot be canceled.')
            record.state = 'canceled'
        return True

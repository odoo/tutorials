from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property Model'

    DEFAULT_BEDROOM_COUNT = 2
    DEFAULT_AVAILABILITY_DATE = fields.Date.today() + relativedelta(months=3)

    name = fields.Char(string='Title', required=True, default='New Property')
    description = fields.Text()
    active = fields.Boolean()
    date_availability = fields.Date(string='Available From', copy=False, default=DEFAULT_AVAILABILITY_DATE)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        default='new',
    )

    bedrooms = fields.Integer(default=DEFAULT_BEDROOM_COUNT)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    living_area = fields.Integer(string='Living Area (sqm)')
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    postcode = fields.Char()

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer')

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
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
            self.garden_orientation = ''

    def action_sold(self):
        CANNOT_SELL_CANCELED_PROPERTY = "You cannot sell a canceled property"
        if self.state == 'canceled':
            raise UserError(CANNOT_SELL_CANCELED_PROPERTY)
        self.state = 'sold'

    def action_cancel(self):
        CANNOT_SELL_SOLD_PROPERTY = "You cannot cancel a sold property"
        if self.state == 'sold':
            raise UserError(CANNOT_SELL_SOLD_PROPERTY)
        self.state = 'canceled'

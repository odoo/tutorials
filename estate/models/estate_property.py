from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models


class Estate(models.Model):
    _name = 'estate.property'
    _description = 'It allows to manage your properties'
    _order = 'id desc'

    name = fields.Char(required=True, default='Unknown')
    property_type_id = fields.Many2one('estate.property.type')
    tag_ids = fields.Many2many('estate.property.tag')
    last_seen = fields.Datetime('Last Seen', default=fields.Datetime.now)
    description = fields.Char(required=True)
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.today() + relativedelta(months=3), copy=False)
    active = fields.Boolean(default=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_offer = fields.Float(compute='_compute_best_offer')
    sales_person_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')
    buyer_id = fields.Many2one('res.partner', string='Customer')
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    living_area = fields.Integer()
    garden_area = fields.Integer()
    total_area = fields.Float(compute='_compute_total_area')
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        readonly=True,
    )

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price >= 0 )', 'A price should always be possitive'),
        ('selling_price', 'CHECK(selling_price >= 0 )', 'A price should always be possitive'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('offer_ids')
    def _onchange_status(self):
        for record in self:
            if record.state not in ['offer accepted', 'sold', 'cancelled']:
                all_status = record.offer_ids.mapped('status')
                new_state = 'new'
                if all_status:
                    new_state = 'offer received'
            record.state = new_state

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            all_price = record.offer_ids.mapped('price')
            if all_price:
                record.best_offer = max(all_price)
            else:
                record.best_offer = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_property_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError('property already cancelled')
            record.state = 'sold'

    def action_property_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError('property already sold')
            record.state = 'cancelled'

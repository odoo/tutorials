from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class TestModel(models.Model):
    _name = 'estate.property'
    _description = 'Test Estate Model'
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=False, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        readonly=True,
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    seller_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False, readonly=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (sqm)')
    best_price = fields.Float(compute='_compute_best_price')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be a strictly positive value.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The expected price must be a positive value'),
        ('unique_tag_name_and_type', 'UNIQUE(name, property_type_id)', 'The Name and the type should be unique.'),
    ]

    @api.constrains('selling_price')
    def _check_date_end(self):
        for record in self:
            if record.state == 'offer_accepted' and float_compare(record.selling_price, 0.9 * record.expected_price, 2):
                raise UserError(self.env._('the seeling price must be atleast 90% of the expected price.'))

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = ''

    def action_sell_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._('Cancelled properties cant be sold'))
            else:
                record.state = 'sold'
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._('Sold properties cant be cancelled'))
            else:
                record.state = 'cancelled'
        return True

    @api.model
    def ondelete(self):
        if self.state in ['new', 'cancelled']:
            return super().ondelete()
        raise UserError(self.env._('You cannot delete a property unless cancelled.'))

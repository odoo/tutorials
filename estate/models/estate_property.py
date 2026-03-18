from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A specific property"

    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From', copy=False, default=lambda _: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    _expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.',
    )
    selling_price = fields.Float(readonly=True, copy=False)
    _selling_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'The selling price must be positive.',
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('east', 'East'),
            ('south', 'South'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received',
            'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.uid)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (sqm)')
    best_price = fields.Float(string='Best Price', compute='_compute_best_price')

    @api.depends('living_area', 'garden_area', 'garden')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + (record.garden_area if record.garden else 0)

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError('A cancelled listing cannot be sold')
            elif record.state == 'sold':
                raise exceptions.UserError('This listing has already been sold')
            else:
                record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError('Sold listings cannot be cancelled')
            elif record.state == 'cancelled':
                raise exceptions.UserError('This listing is already cancelled')
            else:
                record.state = 'cancelled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _validate_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, record.expected_price * 0.9, 2) == -1 and not float_is_zero(record.selling_price, 2):
                raise exceptions.ValidationError('The selling price must be at least 90%% of the expected price')

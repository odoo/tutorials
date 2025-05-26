from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.date_utils import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    name = fields.Char('Name', required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    best_price = fields.Float('Best Offer', compute='_compute_best_price')
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Has Garage')
    garden = fields.Boolean('Has Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    total_area = fields.Float('Total Area (sqm)', compute='_compute_total_area')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new',
    )
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price should be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price should be positive.'),
        ('check_garden_area', 'CHECK(garden = false OR garden_area > 0)', 'The garden area should be strictly positive.'),
        ('check_garden_orientation', "CHECK(garden = false OR garden_orientation IN ('north', 'south', 'east', 'west'))", 'You should choose a garden orientation.'),
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2):
                if record.expected_price:
                    if float_compare(record.selling_price, record.expected_price * 0.9, 2) < 0:
                        raise ValidationError(self.env._('The selling price must be at least 90% of the expected price.'))

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            if record.living_area or record.garden_area:
                record.total_area = 0
                if record.living_area:
                    record.total_area += record.living_area
                if record.garden_area:
                    record.total_area += record.garden_area
            else:
                record.total_area = None

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = None

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            if not self.garden_area:
                self.garden_area = 10
            if not self.garden_orientation:
                self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.onchange('offer_ids')
    def _onchange_offer_ids(self):
        if self.state == 'new':
            if len(self.offer_ids):
                self.state = 'offer_received'

    def action_set_sold(self):
        self.ensure_one()

        if self.state == 'cancelled':
            raise UserError(self.env._('Cancelled properties cannot be sold.'))

        self.state = 'sold'

    def action_set_cancelled(self):
        self.ensure_one()

        if self.state == 'sold':
            raise UserError(self.env._('Sold properties cannot be cancelled.'))

        self.state = 'cancelled'

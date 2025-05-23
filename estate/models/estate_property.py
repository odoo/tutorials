from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real estate property with offers, pricing, and availability.'
    _order = 'id desc'

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive!'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive!'),
    ]

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        'Availability From',
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    best_price = fields.Float('Best Price', compute='_compute_best_price', store=True)
    property_type_id = fields.Many2one('estate.property.type', 'Property Type')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    buyer_id = fields.Many2one('res.partner', 'Buyer')
    seller_id = fields.Many2one('res.users', 'Seller', default=lambda self: self.env.user)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        'Garden Orientation',
    )
    total_area = fields.Integer('Total Area (sqm)', compute='_compute_total_area', store=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        'State',
        default='new',
        required=True,
        copy=False,
    )
    offer_ids = fields.One2many('estate.property.offer', 'property_id', 'Offers')
    active = fields.Boolean('Active', default=True)

    ###### COMPUTE ######
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            if prices:
                record.best_price = max(prices)
            else:
                record.best_price = 0.0

    ###### ONCHANGE ######
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    ###### CRUD ######
    def unlink(self):
        if any(record.state not in ['new', 'cancelled'] for record in self):
            raise UserError(_('You cannot delete a property that is not new or cancelled.'))
        return super().unlink()

    ###### ACTION ######
    def action_sold(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('Property is already sold.'))
            if record.state == 'cancelled':
                raise UserError(_('Property is cancelled and cannot be sold.'))
            if record.state != 'offer_accepted':
                raise UserError(_('You must accept an offer before marking the property as sold.'))

            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_('Property is already cancelled.'))
            if record.state == 'sold':
                raise UserError(_('Sold properties cannot be cancelled.'))

            record.state = 'cancelled'
        return True

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Property'
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The Expected Price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The Selling Price must be positive.'),
        ('check_bedrooms', 'CHECK(bedrooms >= 0)', 'The number of bedrooms must be positive.'),
        ('check_living_area', 'CHECK(living_area > 0)', 'The living area must be positive.'),
        ('check_facades', 'CHECK(facades > 0)', 'The number of facades must be positive.'),
        ('check_name_unique', 'UNIQUE(name)', 'The Property name must be unique.')
    ]
    _order = 'id desc'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string='Available From', copy=False,
                                    default=lambda self: fields.Datetime.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (m²)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (m²)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('east', 'East'),
        ('south', 'South'),
        ('west', 'West')
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new', required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', required=True)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Sales Person', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(string='Total Area (m²)', compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids) == 0:
                record.best_price = 0
            else:
                record.best_price = max(record.offer_ids.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = None
            self.garden_area = 0

    @api.constrains('selling_price', 'expected_price')
    def _check_date_end(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price,
                                                                                             0.9 * record.expected_price,
                                                                                             precision_digits=2) >= 0:
                raise ValidationError("The selling price must not be below 90% of the expected price.")

    def action_sold(self):
        for record in self:
            if record.state in ['sold', 'canceled']:
                raise UserError('Cannot mark as sold.')
            record.state = 'sold'
        return True

    def action_canceled(self):
        for record in self:
            if record.state in ['sold', 'canceled']:
                raise UserError('Cannot mark as canceled.')
            record.state = 'canceled'
        return True

    def action_reset(self):
        for record in self:
            if record.state not in ['sold', 'canceled']:
                raise UserError('Cannot reset.')
            record.state = 'new'
        return True

    # Make sure that only one offer is accepted
    def set_accepted_offer(self, offer):
        for record in self:
            if offer is not None:
                record.state = 'offer_accepted'
                record.selling_price = offer.price
                record.buyer_id = offer.partner_id
            else:
                record.state = 'offer_received'
                record.selling_price = 0
                record.buyer_id = None
            for o in record.offer_ids:
                if o.state == 'accepted' and (offer is None or o.id != offer.id):
                    o.action_reset(propagate=False)

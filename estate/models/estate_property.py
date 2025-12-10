from odoo import models, fields, api, exceptions
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = 'Estate Property details'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new',
        required=True,
        copy=False
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    buyer = fields.Many2one('res.partner', copy=False)
    salesperson = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price') or [0])

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = None
            self.garden_area = 0

    def cancel_property_sale(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError('A sold property cannot be cancelled')
            else:
                record.state = 'cancelled'
        return True

    def set_property_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError('A cancelled property cannot be Sold')
            else:
                record.state = 'sold'
        return True

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The Expected price cannot be 0 or less then 0'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The Selling price cannot be less then 0'
    )

    @api.constrains('selling_price', 'buyer', 'expected_price')
    def _check_selling_price_90p(self):
        for record in self:
            if record.selling_price == 0:
                return False
            if float_compare((record.selling_price / record.expected_price) * 100, 90, precision_digits=2) < 0:
                raise exceptions.ValidationError('Selling Price should be 90% or more of expected price.')

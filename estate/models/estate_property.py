from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(
        string='Availability Date',
        default=lambda self: fields.Date.today() + timedelta(days=90),
        copy=False
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades of Property')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], required=True, default='new', copy=False)
    property_type_id = fields.Many2one(
        'estate.property.type', string="Property")
    buyer_id = fields.Many2one(
        'res.partner', string="Buyer")
    sell_person_id = fields.Many2one(
        'res.users', string="Seller", default=lambda self: self.env.user)
    tag_ids = fields.Many2many(
        'estate.property.tag', string="Tags")
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Float(string="Total area", compute='_compute_total_area')
    # total_area = fields.Float(compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer Price', compute='_compute_best_price')

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            offer_prices = record.offer_ids.mapped('price')
            record.best_price = max(offer_prices, default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled property cannot be set as sold.")
            record.state = 'sold'

    def action_set_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold property cannot be canceled.")
            record.state = 'canceled'

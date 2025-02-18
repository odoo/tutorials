from odoo import fields, models, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "this is the estate property model"
    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From', default=fields.Date.today() + relativedelta(months=5), copy=False)
    expected_price = fields.Float(digits=(20, 2), required=True)
    selling_price = fields.Float(digits=(20, 2), readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')])
    state = fields.Selection(string='Status', selection=[
        ('new', 'New'),
        ('offer', 'Offer'),
        ('received', 'Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], copy=False, required=True, default='new')
    active = fields.Boolean(default=True)

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', copy=False, string='Buyer')
    salesman_id = fields.Many2one('res.users', default=lambda self: self.env.user, string='Salesman')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer('Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float('Best Offer', digits=(20, 2), compute='_compute_best_price')

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            best_price = 0.0
            for offer in record.offer_ids:
                if (offer.price > best_price):
                    best_price = offer.price
            record.best_price = best_price

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = None
            self.garden_orientation = None
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Cancelled properties cannot be sold')
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be cancelled')
            record.state = 'cancelled';
        return True

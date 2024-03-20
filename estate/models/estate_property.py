# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions
from odoo.tools import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero

DEFAULT_GARDEN_AREA = 10

class EstateProperty(models.Model):

    def _get_default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)

    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new', required=True, copy=False)

    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesman_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", default=_get_default_date_availability, copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)

    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])

    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price must be positive')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.mapped('offer_ids.price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = DEFAULT_GARDEN_AREA
            self.garden_orientation = 'north'

    def action_cancel(self):
        self.ensure_one()

        if self.state == 'sold':
            raise exceptions.UserError("Sold properties cannot be canceled!")

        return self.write({'state': 'canceled'})

    def action_sold(self):
        self.ensure_one()

        if self.state == 'canceled':
            raise exceptions.UserError("Canceled properties cannot be sold!")

        return self.write({'state': 'sold'})

    def accept_offer(self, price, partner_id):
        self.ensure_one()
        self.selling_price = price
        self.buyer_id = partner_id

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                raise exceptions.ValidationError("The selling price cannot be lower than 90% of the expected price.")

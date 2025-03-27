from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'
    _sql_constraints = [
        (
            'expected_price_strictly_positive',
            'CHECK(expected_price > 0)',
            'Expected price must be strictly positive',
        ),
        (
            'selling_price_positive',
            'CHECK(selling_price >= 0)',
            'Selling price must be positive',
        ),
    ]

    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
    )
    buyer_id = fields.Many2one(
        'res.partner',
        compute='_compute_infos_from_accepted_offer',
        string='Buyer',
        copy=False,
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
        copy=False,
    )
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Float(compute='_compute_total_area', string='Total Area (sqm)')
    best_offer = fields.Float(compute='_compute_best_offer', string='Best Offer')
    active = fields.Boolean(default=True)
    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(
        string='Available From',
        copy=False,
        default=date.today() + relativedelta(months=3),  # noqa: DTZ011
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(
        compute='_compute_infos_from_accepted_offer',
        string='Selling Price',
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Number of Facades')
    garage = fields.Boolean(string='Has Garage?')
    garden = fields.Boolean(string='Has Garden?')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string='Garden Orientation',
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        required=True,
        copy=False,
        default='new',
    )
    note = fields.Text('Special mentions about the house')

    @api.depends('offer_ids.status')
    def _compute_infos_from_accepted_offer(self):
        for property in self:
            for offer in property.offer_ids:
                if offer.status == 'accepted':
                    property.buyer_id = offer.partner_id
                    property.selling_price = offer.price
                    return
            property.buyer_id = None
            property.selling_price = None

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            if property.offer_ids:
                property.best_offer = max(map(lambda r: r.price, property.offer_ids))
            else:
                property.best_offer = None

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for property in self:
            if not float_is_zero(property.selling_price, precision_digits=2):
                if (
                    float_compare(
                        property.selling_price,
                        property.expected_price * 0.9,
                        precision_digits=2,
                    )
                    < 0
                ):
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price!")

    @api.onchange('garden')
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_only_new_and_cancelled(self):
        if any(property.state != 'new' and property.state != 'cancelled' for property in self):
            raise UserError("Can't delete if state is not New or Cancelled!")

    def action_sold(self):
        for property in self:
            if property.state != 'cancelled':
                property.state = 'sold'
                return True
            raise UserError("A cancelled property cannot be set as sold")

    def action_cancel(self):
        for property in self:
            if property.state != 'sold':
                property.state = 'cancelled'
                return True
            raise UserError("A sold property cannot be set as cancelled")

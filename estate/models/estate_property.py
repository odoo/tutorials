from dateutil import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'
    _order = 'id desc'

    name = fields.Char(string='Name of the Property', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(
        string='Available From',
        copy=False,
        default=fields.Date.today() + relativedelta.relativedelta(months=3),
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Number Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
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
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    users_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', readonly=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer', compute='_compute_price')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must strictly be positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
    ]

    @api.ondelete(at_uninstall=False)
    def prevent_delete_based_on_state(self):
        if any(record.state in {'new', 'cancelled'} for record in self):
            raise UserError(_('A new or cancelled property cannot be deleted.'))

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_price(self):
        for record in self:
            record.write({'best_price': max(record.offer_ids.mapped('price'), default=0)})

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.write({'garden_orientation': False, 'garden_area': 0})
            return

        self.write({'garden_area': 10, 'garden_orientation': self.garden_orientation or 'north'})

    def action_sell(self):
        if 'cancelled' in self.mapped('state'):
            raise UserError(_('A property cancelled cannot be set as sold.'))

        self.write({'state': 'sold'})
        return True

    def action_cancel(self):
        if 'sold' in self.mapped('state'):
            raise UserError(_('A property sold cannot be set as cancelled.'))

        self.write({'state': 'cancelled'})
        return True

    @api.constrains('selling_price')
    def _check_price(self):
        for record in self:
            if not record.selling_price:
                continue

            if float_utils.float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=3) == -1:
                raise ValidationError(_('The selling cannot be lower than 90% of the expected price.'))

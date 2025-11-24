from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Property'
    _order = 'id desc'

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        'Available From',
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=+3),
    )
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        default='north',
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Types')
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user
    )
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string='Property Offers'
    )
    total_area = fields.Integer('Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float('Best Offer', compute='_compute_best_price')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'
    )

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.garden_area + property.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            if property.state != 'offer_accepted':
                continue

            if (
                property.state == 'offer_accepted'
                and float_compare(property.selling_price, 0, 2) == -1
            ):
                raise ValidationError('The selling price must be positive.')

            if (
                float_compare(property.selling_price, property.expected_price * 0.9, 2)
                == -1
            ):
                raise ValidationError(
                    'Selling cannot be less than 90% of the expected price.'
                )

    @api.ondelete(at_uninstall=False)
    def delete(self):
        for property in self:
            if property.state not in ('new', 'canceled'):
                raise UserError(
                    'Only properties in New or Canceled state can be deleted.'
                )

    def action_set_property_as_sold(self):
        for property in self:
            if property.state == 'canceled':
                raise UserError('Canceled properties cannot be sold.')
            property.state = 'sold'
        return True

    def action_set_property_as_canceled(self):
        for property in self:
            if property.state == 'sold':
                raise UserError('Sold properties cannot be canceled.')
            property.state = 'canceled'
        return True

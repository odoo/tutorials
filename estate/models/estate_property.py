from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string='Available From',
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
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
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        string='Property Type',
        index='btree_not_null',
    )
    buyer_id = fields.Many2one(comodel_name='res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
        index=True,
    )
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string='Tags')
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        string='Offers',
    )
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive.',
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for estate_property in self:
            estate_property.total_area = estate_property.living_area + estate_property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for estate_property in self:
            estate_property.best_price = max(estate_property.offer_ids.mapped('price'), default=0)

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_ratio(self):
        """Forbid selling below 90% of the expected price (0 means no offer accepted yet)."""
        for estate_property in self:
            if float_is_zero(estate_property.selling_price, precision_digits=2):
                continue
            min_price = estate_property.expected_price * 0.9
            if float_compare(estate_property.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(self.env._(
                    'The selling price cannot be lower than 90% of the expected price.',
                ))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_cancelled(self):
        if any(state not in ('new', 'cancelled') for state in self.mapped('state')):
            raise UserError(self.env._('Only new or cancelled properties can be deleted.'))

    def action_cancel(self):
        if 'sold' in self.mapped('state'):
            raise UserError(self.env._('Sold properties cannot be cancelled.'))
        self.state = 'cancelled'
        return True

    def action_sold(self):
        if 'cancelled' in self.mapped('state'):
            raise UserError(self.env._('Cancelled properties cannot be sold.'))
        self.state = 'sold'
        return True

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'An individual estate property listing'
    _order = 'id desc'
    _sql_constraints = [
        (
            'estate_property_expected_price_positive',
            'CHECK(expected_price > 0)',
            'The expected price must be strictly positive.',
        ),
        (
            'estate_property_selling_price_non_negative',
            'CHECK(selling_price >= 0)',
            'The selling price must be non negative.',
        ),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2) and (
                float_compare(record.selling_price, (record.expected_price * 0.9), 2)
                == -1
            ):
                raise ValidationError(
                    'The selling price must be greater than 90% of the expected price. You must reduce the expected '
                    'price if you want to accept this offer'
                )

    name = fields.Char('Title', required=True, default='Unknown')
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        'Available From',
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', copy=False, readonly=True)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        'Garden Orientation',
    )
    last_seen = fields.Datetime('Last Seen', default=fields.Datetime.now)
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        'Status',
        default='new',
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one('estate.property.type', 'Property Type')
    salesperson_id = fields.Many2one(
        'res.users', 'Salesperson', default=lambda self: self.env.uid
    )
    buyer_id = fields.Many2one('res.partner', 'Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    best_price = fields.Float(
        'Best Price', copy=False, readonly=True, compute='_compute_best_price'
    )
    total_area = fields.Integer(
        compute='_compute_total_area', readonly=True, string='Total Area (sqm)'
    )

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = (
                max(record.offer_ids.mapped('price')) if record.offer_ids else 0
            )

    @api.onchange('garden')
    def _onchange_garden(self):
        """Set default garden area and orientation when garden is checked."""
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.onchange('offer_ids')
    def _onchange_offer_ids(self):
        # When the user removes all offers
        if not self.offer_ids:
            if self.state == 'offer_received':
                self.state = 'new'
            elif self.state == 'offer_accepted':
                # Check if the accepted offer was removed
                self.state = 'new'
                self.selling_price = 0
                self.buyer_id = False
            return

        # User created the first offer
        if self.state == 'new':
            self.state = 'offer_received'
            return

        # User removed an offer when the property was in offer_accepted state
        if self.state == 'offer_accepted':
            # Check if the accepted offer was removed
            if not self.offer_ids.filtered(lambda o: o.status == 'accepted'):
                self.selling_price = 0
                self.buyer_id = False
                self.state = 'offer_received'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('You cannot cancel a sold property.')

            record.state = 'cancelled'

        return True

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('You cannot mark a cancelled property as sold.')

            record.state = 'sold'

        return True

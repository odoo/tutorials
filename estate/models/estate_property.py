from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    property_tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    date_availability = fields.Date(
        'Available From',
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)

    bedrooms = fields.Integer('# Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean('Garage')

    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )

    total_area = fields.Float(string='Total Area', compute='_compute_total_area')

    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.uid)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    best_offer = fields.Float(string='Best Offer', compute='_compute_best_offer')

    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        default='new',
        required=True
    )

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property should be stricly positive'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price of a property should be positive'
    )

    @api.constrains('state', 'expected_price', 'selling_price')
    def _check_prices(self):
        for record in self:
            if record.state == 'offer_accepted' \
            and float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                raise ValidationError('The selling price must be at least 90% of the selling price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sell(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Canceled properties cannot be sold')

            record.state = 'sold'

        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be canceled')

            record.state = 'canceled'

        return True

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError('Only new and canceled properties can be deleted')

    def set_offer_received(self):
        for record in self:
            if record.state == 'new':
                record.state = 'offer_received'

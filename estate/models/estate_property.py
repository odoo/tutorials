from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"
    _order = "id desc"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date', copy=False, default=fields.Datetime.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Leaving Area (sqm)')
    facades = fields.Integer('Facade')
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
        ])
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new')

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive'),
    ]

    # Offers
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        string='Offers')

    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    best_offer_price = fields.Integer(string='Best Offer', default=0, compute='_compute_best_offer_price')

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_offer_price(self):
        for record in self:
            record.best_offer_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_set_sold_property(self):
        if self.state == 'canceled':
            raise UserError('Canceled property cannot be sold')
        self.state = 'sold'

    def action_set_cancel_property(self):
        if self.state == 'sold':
            raise UserError('sold property cannot be Canceled')
        self.state = 'canceled'

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2) and float_compare(record.selling_price, record.expected_price * 0.9, 2) == -1:
                raise ValidationError("selling price cannot be lower than 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_offered_property(self):
        if any(record.state not in ['new', 'canceled'] for record in self):
            raise UserError('You can not delete a property in an offered state')

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    active = fields.Boolean(string='Active', default=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    best_price = fields.Float(compute='_compute_best_price')
    buyer = fields.Many2one(comodel_name='res.partner', readonly=True, string='Buyer', copy=False)
    date_availability = fields.Date(
        string='Date availability',
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )
    description = fields.Text(string='Description')
    expected_price = fields.Float(string='Expected price', required=True)
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden area')
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    living_area = fields.Integer(string='Living area')
    name = fields.Char(string='Name', required=True, default="Unknown")
    offers = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string='Offers')
    postcode = fields.Char(string='Postcode')
    property_type = fields.Many2one(comodel_name='estate.property.type', string='Property type')
    salesperson = fields.Many2one(comodel_name='res.users', string='Salesperson', default=lambda self: self.env.user)
    selling_price = fields.Float(string='Selling price', readonly=True, copy=False)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=True,
        default='new',
    )
    tags = fields.Many2many(comodel_name='estate.property.tag', string='Tags')
    total_area = fields.Integer(compute='_compute_total_area')

    _strictly_positive_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property should be strictly positive.',
    )
    _positive_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price of a property should be positive.',
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offers.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offers.mapped('price')) if record.offers else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def sold_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._('A cancelled property cannot be sold.'))
            record.state = 'sold'
        return True

    def cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._('A sold property cannot be cancelled.'))
            record.state = 'cancelled'
        return True

    def action_view_offers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'name': self.env._('Offers'),
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('property_id', '=', self.id)],
        }

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price_relation_to_expected_price(self):
        for record in self:
            if float_compare(record.expected_price * 0.9, record.selling_price, 2) == 1 and not float_is_zero(record.selling_price, 2):
                raise ValidationError(self.env._(r'The selling price cannot be lower than 90% of the expected price.'))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_status_is_new_or_cancelled(self):
        if any(record.state not in ['new', 'cancelled'] for record in self):
            raise UserError(self.env._('Can\'t delete a property that is not new or cancelled.'))

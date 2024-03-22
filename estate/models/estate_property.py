from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate Property Field"
    _order = "id desc"

    name = fields.Char(required=True, string='Title')
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), days=90), string='Available From')
    expected_price = fields.Float(required=True, string='Expected Price')
    selling_price = fields.Float(readonly=True, copy=False, string='Selling Price')
    bedrooms = fields.Integer(default=2, string='Bedrooms')
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(
        default='new',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')])
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (sqm)')
    best_price = fields.Float(compute='_compute_best_price', string='Best Offer')

    _sql_constraints = [
        ('check_strict_positive_exptected_price',
            'CHECK(expected_price > 0)',
            'The expected price should be strictly positive'),
        ('check_positive_selling_price',
            'CHECK(selling_price >= 0)',
            'The selling price should be positive'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_set_sold_state(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(message='A canceled property can not be sold')
            record.state = 'sold'
        return True

    def action_set_canceled_state(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(message='A sold property can not be canceled')
            record.state = 'canceled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, 0.9*record.expected_price, precision_digits=2) < 0:
                    raise ValidationError(message="The selling price must be greater than 90% of exptected price")

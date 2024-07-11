from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char('Property Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        copy=False,
        default='new'
    )
    expected_price = fields.Float('Expected Price', required=True)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West'), ('select', 'Select')],
        default='select'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    seller_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    total = fields.Float('Total Area (sqm)', compute="_compute_total")
    best_price = fields.Float('Best Offer', compute="_compute_offer")

    _sql_constraints = [
            ('check_expected_price', 'CHECK(expected_price > 0)',
            'The expected price must be positive'),
            ('check_selling_price', 'CHECK(selling_price >= 0)',
            'The selling price must be positive')
        ]

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Canceled properties cannot be sold.')
            else:
                self.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be canceled.')
            else:
                self.state = 'canceled'

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, ((0.9) * record.expected_price), precision_digits=2) == -1:
                raise ValidationError("the selling price cannot be lower than 90 percent of the expected price")

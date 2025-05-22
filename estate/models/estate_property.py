from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positve'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive')
    ]
    _order = 'id desc'

    name = fields.Char('Name', required=True)
    description = fields.Char('Description')
    post_code = fields.Char('Post Code')
    state = fields.Selection(
        string="State",
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="Estate current state",
        required=True,
        default='new',
        copy=False
    )
    date_availability = fields.Date('Available From', copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    best_price = fields.Float('Best Price', compute='_compute_best_price')
    bedrooms = fields.Integer('Bedrooms Count', default=2)
    living_area = fields.Float('Living Area size')
    facades = fields.Integer('Number of facades')
    garage = fields.Boolean('Has garage')
    garden = fields.Boolean('Has garden')
    garden_area = fields.Float('Garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Garden orientation selection"
    )
    total_area = fields.Float('Total Area', compute='_compute_total_area')
    active = fields.Boolean('Is Active', default=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', 'Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', 'Salesperson', index=True, default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0

    @api.onchange('garden')
    def _onchange_garden_checkbox(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else None

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_is_new_or_canceled(self):
        invalid_records = self.filtered(lambda r: r.state not in ('new', 'canceled'))
        if invalid_records:
            raise UserError("You can only delete properties in NEW or CANCELED state.")

    def action_set_sold(self):
        for record in self:
            if (record.state == 'sold'):
                raise UserError('Property Already Sold')
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise UserError("Cannot sell a canceled property")
        return True

    def action_set_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Cannot cancel a sold property')
            if (record.state == 'canceled'):
                raise UserError("Property Already canceled")
            record.state = 'canceled'
        return True

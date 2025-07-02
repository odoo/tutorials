from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _sql_constraints = [
        ('expected_price_positive',
         'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('selling_price_positive',
         'CHECK(selling_price >= 0)',
         'The selling price must be positive.')
    ]

    # misc
    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string='Available From',
        default=fields.Date.add(fields.Date.today(), months=3), copy=False)

    # price
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)

    # area
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')])

    # reserved
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')],
        string="Status", required=True, default='new', copy=False)

    # many2one
    property_type_id = fields.Many2one('estate.property.type',
                                       string='Property Type')
    salesman = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', copy=False)
    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    # many2many
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    # one2many
    offer_ids = fields.One2many('estate.property.offer',
                                'property_id',
                                string='Offers')

    # computed
    total_area = fields.Integer(compute='_compute_total_area',
                                string='Total Area (sqm)')
    best_offer = fields.Float(compute='_compute_best_offer')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'),
                                    default=0)

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_margin(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue

            min_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_price,
                             precision_rounding=0.01) < 0:
                raise ValidationError(
                    'The selling price must be at least'
                    ' 90% of the selling price!'
                    'You must reduce the expected price '
                    'if you want to accept this offer.')

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_only_for_new_or_cancelled(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError(
                    'Only new and cancelled properties can be deleted.')

    def action_sell_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Cancelled property cannot be sold.')

            record.state = 'sold'
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold property cannot be cancelled.')

            record.state = 'cancelled'
        return True

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability', default=fields.Datetime.add(
        fields.Datetime.today(), months=3), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new'
    )
    property_type_id = fields.Many2one(
        'estate.property.type', string='Property Type')
    buyer = fields.Many2one('res.partner', string='Buyer')
    salesperson = fields.Many2one(
        'res.users', string='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string='Offers')

    total_area = fields.Float('Total Area', compute='_compute_total_area')
    best_offer = fields.Float('Best Offer', compute='_compute_best_offer')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price must be positive'),
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.buyer is not None and not float_is_zero(record.expected_price, precision_digits=2):
                percent = (record.selling_price * 100) / \
                    (record.expected_price)
                if float_compare(percent, 90.0, precision_digits=2) == -1:
                    raise ValidationError(
                        "The selling must be 90% of the expected price. You must update your offer price.")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price')) if hasattr(
                record, 'offer_ids') and len(record.offer_ids) > 0 else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.write({
                'garden_area': 10,
                'garden_orientation': 'north'
            })
        else:
            self.write({
                'garden_area': 0,
                'garden_orientation': None
            })

    @api.ondelete(at_uninstall=False)
    def _unlink_except_property_sold_cancelled(self):
        for record in self:
            if record.state != 'new' and record.state != 'cancelled':
                raise UserError(
                    'Only new and cancelled property can be deleted')

    def action_set_property_sold(self):
        if self.state == 'cancelled':
            raise UserError("Cancelled properties cannot be sold")
        self.state = 'sold'

    def action_set_property_cancelled(self):
        if self.state == 'sold':
            raise UserError("Sold properties cannot be cancelled")
        self.state = 'cancelled'

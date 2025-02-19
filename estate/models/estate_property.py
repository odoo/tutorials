from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "this is the estate property model"
    _sql_constraints = [
        ('check_positive_amounts',
         'CHECK (expected_price > 0 AND selling_price >= 0)',
         'This amount must be positive'),
    ]
    _order = 'id desc'

    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From', default=fields.Date.today() + relativedelta(months=5), copy=False)
    expected_price = fields.Float(digits=(20, 2), required=True, default=1000)
    selling_price = fields.Float(digits=(20, 2), readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        copy=False,
        required=True,
        default='new',
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', copy=False, string='Buyer')
    salesman_id = fields.Many2one('res.users', default=lambda self: self.env.user, string='Salesman')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer('Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float('Best Offer', digits=(20, 2), compute='_compute_best_price')

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price') + [0.0])

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = None
            self.garden_orientation = None
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'

    def action_sold(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold")
            property.state = 'sold'
        return True

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("Sold properties cannot be cancelled")
            property.state = 'cancelled';
        return True

    @api.constrains('selling_price')
    def _check_offer_good_enough(self):
        for property in self:
            if float_compare(property.selling_price, .9 * property.expected_price, precision_digits=10) < 0:
                raise ValidationError("The selling price must be at least 90% of the expected price")

    @api.ondelete(at_uninstall=True)
    def _unlink_estate_property(self):
        if self.filtered(lambda property: property.state not in ('new', 'cancelled')):
            raise UserError("Removing a property is not allowed if it is neither new nor cancelled")


from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare
from odoo.fields import Many2many, One2many

from .helper import format_selection


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property modelisation'
    _order = 'id desc'
    _sql_constraints = [
        ('expected_price_strictly_positive', 'CHECK(expected_price > 0)', 'Expected price must be stricly positive'),
        ('selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling price must be positive'),
    ]

    name = fields.Char(required=True, string="Name")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postal code")
    date_availability = fields.Date(default=lambda x: fields.Date.today() + relativedelta(months=3), copy=False,
                                    string='Availability date')
    expected_price = fields.Float(required=True, string='Expected price')
    selling_price = fields.Float(readonly=True, copy=False, string='Selling price')
    bedrooms = fields.Integer(default=2, string='Bedrooms')
    living_area = fields.Integer(string='Living area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden area')
    garden_orientation = fields.Selection(string='Orientation',
                                          selection=format_selection(['north', 'south', 'east', 'west']),
                                          )
    active = fields.Boolean(default=True, string='Active')
    state = fields.Selection(string='State',
                             selection=format_selection(
                                 ['new', 'offer received', 'offer accepted', 'sold', 'canceled']),
                             default='new')

    property_type_id = fields.Many2one('estate.property.type', string='Property type')

    buyer_id = fields.Many2one('res.partner', copy=False, string='Buyer')
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user, string='Salesperson')

    tag_ids = Many2many('estate.property.tag', string='Tags')
    offer_ids = One2many('estate.property.offer', 'property_id', string='Offers')

    total_area = fields.Integer(compute='_compute_total_area', string='Total area')
    best_price = fields.Float(compute='_compute_best_price', string='Best offer price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for estate in self:
            estate.best_price = max(estate.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden = [0, 10][self.garden]
        self.garden_orientation = ['', 'north'][self.garden]

    @api.constrains('selling_price')
    def _check_price_offer_reasonable(self):
        if float_compare(self.selling_price, 0.9 * self.expected_price, 3) <= 0:
            raise ValidationError('The selling price must be at least 90% of the expected price.')

    @api.ondelete(at_uninstall=False)
    def _unlink_property_if_not_new_nor_canceled(self):
        self.ensure_one()
        if self.state not in ('new', 'canceled'):
            raise UserError('Only new and canceled properties can be deleted.')

    def action_sold(self):
        self.ensure_one()
        if self.state == 'canceled':
            raise UserError('Canceled properties cannot be sold.')
        self.state = 'sold'
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'sold':
            raise UserError('Sold properties cannot be canceled.')
        self.state = 'canceled'
        return True

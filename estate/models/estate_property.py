from odoo import api, models, fields
from datetime import date, timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is Real Estate"
    _order = "id desc"

    name = fields.Char('property Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date availability', copy=False, default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float('expected price', required=True)
    selling_price = fields.Float('sell price', readonly=True, copy=False)
    bedrooms = fields.Integer('bedrooms', default=2)
    living_area = fields.Integer('live area')
    facades = fields.Integer('facades')
    garage = fields.Boolean('garage')
    garden = fields.Boolean('garden')
    garden_area = fields.Integer('garden area')
    garden_orientation = fields.Selection(
        string='Garden direction',
        selection=[('north', 'North'),
                ('south', 'South'),
                ('east', 'East'),
                ('west', 'West')
            ]
    )
    state = fields.Selection(
        string='state',
        selection=[('new', 'New'),
                ('offer_received', 'Offer Received'),
                ('offer_accepted', 'Offer Accepted'),
                ('sold', 'Sold'),
                ('canceled', 'Canceled')],
        required=True,
        default='new',
        copy=False
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="property type"
    )
    salesperson_id = fields.Many2one("res.users", string="Sales person", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="property offer")

    total_area = fields.Float(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(string="Best Offer Price", compute="_compute_best_price")

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be set as canceled")
            else:
                record.state = 'canceled'

    def action_sold(self):
        for record in self:
            if not record.buyer_id:
                raise UserError('You cannot sell a property without assigning a customer.')
            if record.state == 'canceled':
                raise UserError("A canceled property cannot be sold.")
            else:
                record.state = 'sold'

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'expected price must be strictly positive'),
         ('cheselling_price', 'CHECK(selling_price >= 0)', 'selling price must be positive')
    ]

    @api.constrains('selling_price', 'expected_price')
    def check_price(self):
        if float_compare(self.selling_price, 0.9 * self.expected_price, 2) == -1 and not float_is_zero(self.selling_price, 2):
            raise ValidationError('selling price must greater than 90% of expected price')

    @api.model
    @api.ondelete(at_uninstall=False)
    def _check_state_before_delete(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError('You cannot delete a property that is not in "New" or "Canceled" state.')

    configsold = fields.Boolean(string="Sold Config", compute='_compute_action_sold')

    @api.depends('state')
    def _compute_action_sold(self):
        canbesold = self.env['ir.config_parameter'].sudo().get_param('estate.sold')
        for record in self:
            record.configsold = canbesold == 'True'

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

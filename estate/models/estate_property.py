from dateutil import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is the model for estate properties"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    availability_date = fields.Date(copy=False, default=fields.Date.today() + relativedelta.relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
    )
    active = fields.Boolean(default=True)
    status = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new',
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute="_compute_area")
    best_price = fields.Float(compute="_compute_best_price")
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'Selling price must be positive.'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        if (self.status != 'cancelled') & (not float_utils.float_is_zero(self.selling_price, 1)):
            self.status = 'sold'
        else:
            raise UserError("You can't sell this property")
        return True

    def action_cancel(self):
        if self.status != 'sold':
            self.status = 'cancelled'
        else:
            raise UserError("Sold properties can not be cancelled")
        return True

    @api.constrains('selling_price')
    def _check_date_end(self):
        for record in self:
            if (record.status != 'new') & (float_utils.float_compare(record.selling_price, 0.9 * record.expected_price, 1) == -1):
                raise ValidationError("selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_user_inactive(self):
        if (self.status == 'cancelled') | (self.status == 'new'):
            raise UserError("Can't delete new or cancelled property")

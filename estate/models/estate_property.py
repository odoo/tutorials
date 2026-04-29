from odoo import _, api, fields, models
from odoo.tools import date_utils, float_compare, float_is_zero

from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property for purchasing and selling properties"
    _order = "id desc"

    name = fields.Char(required=True, string="Property Name")
    description = fields.Char()
    postcode = fields.Char()
    date_availibility = fields.Date(copy=False, default=lambda x: fields.Date.today() + date_utils.get_timedelta(3, "month"))
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
            ('west', 'West'),

        ],
        default='north'
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer received'),
            ('offer accepted', 'Offer accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new'
    )
    active = fields.Boolean(default=True)
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price', store=True)
    property_type_id = fields.Many2one("estate.property.type")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    _check_positive = models.Constraint(
        'check(expected_price > 0 )',
        'Expected price  must be positive'
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')

            if prices:
                record.best_price = max(prices)
            else:
                record.best_price = 0

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_90(self):
        if float_is_zero(self.selling_price, precision_digits=2):
            return
        if float_compare(self.selling_price, 0.9 * self.expected_price, precision_digits=2) == -1:
            raise ValidationError(_('Offer price should not be lower then 90% of expected price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.ondelete(at_uninstall=False)
    def _prevent_property_deletion(self):
        if self.state not in ['new', 'cancelled']:
            raise UserError(_("You can only delete property if it's in either new or cancelled state"))
        return True

    def action_sold_property(self):
        if self.state != 'offer accepted':
            raise UserError(_("The property cannot be set as sold because the offer is not accepted yet."))
            return False
        if self.state == 'cancelled':
            raise UserError(_("A cancelled property cannot be set as sold."))
            return False

        self.state = 'sold'
        return True

    def action_cancel_property(self):
        if self.state == 'sold':
            raise UserError(_("A sold property cannot be set as cancelled."))

        self.state = 'cancelled'
        return True

from dateutil.relativedelta import *

from odoo import fields, models, api, exceptions, _
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "The properties of real estate"
    _order = "id desc"
    _sql_constraints = [
        (
            'check_expected_price',
            'CHECK(expected_price > 0)',
            'The expected price must be strictly positive.',
        ),
        (
            'check_selling_price',
            'CHECK(selling_price >= 0)',
            'The selling price must be strictly positive.',
        ),
    ]

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[
            ('new', 'New'),
            ('offer-received', 'Offer Received'),
            ('offer-accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one(
        'res.users', string='Salesman', default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(
        string="Total Area (sqm)", compute="_compute_total_area"
    )
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if (
                float_compare(
                    record.selling_price,
                    record.expected_price * 0.90,
                    precision_digits=2,
                )
                == -1
                and float_is_zero(record.selling_price, precision_rounding=2) == False
            ):
                raise exceptions.ValidationError(
                    "The selling price must be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer"
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_or_canceled(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise exceptions.UserError(
                    "Only new and canceled properties can be deleted"
                )

    def action_set_state_sold(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
                return True
            else:
                raise exceptions.UserError(_('Canceled properties cannot be sold'))

    def action_set_state_canceled(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
                return True
            else:
                raise exceptions.UserError(_('Sold properties cannot be canceled'))

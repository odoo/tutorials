from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = 'estate.property'
    _description = 'estate property details'
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.today() + timedelta(days=90)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('west', "West"),
            ('east', "East"),
            ('south', "South"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default='new',
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one(
        'estate.property.type', string="Property Type")
    user_id = fields.Many2one('res.users', string="Salesperson")
    partner_id = fields.Many2one('res.partner', string="Buyer", readonly=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id')
    total_area = fields.Integer(
        compute='_compute_total_area', string="Total Area(sqm)")
    best_price = fields.Float(compute='_compute_best_price', store=True)

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        "The Expected price cannot be negative or zero."
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)',
        "The Selling price cannot be negative."
    )

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        self.total_area = self.living_area + self.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids.mapped('price'):
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = None

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.constrains('selling_price', 'expected_price')
    def _constraint_selling_price(self):
        if float_is_zero(self.selling_price, precision_rounding=0.01):
            return
        if float_compare(self.selling_price, self.expected_price * 0.9, precision_rounding=0.01) < 0:
            raise ValidationError(
                "Selling price cannot be lower than 90% of the expected price.")

    def action_property_sold(self):
        if self.state == 'cancelled':
            raise UserError("Cancelled property cannot be sold.")
        else:
            self.state = "sold"

    def action_property_cancel(self):
        if self.state == 'sold':
            raise UserError("Sold property cannot be Cancelled.")
        else:
            self.state = "cancelled"

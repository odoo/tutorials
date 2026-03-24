# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "estate property"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")])
    total_area = fields.Integer(compute='_compute_total_area')
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string="House Type")
    buyer_id = fields.Many2one(comodel_name='res.partner', string="Buyer", copy=False)
    seller_id = fields.Many2one(comodel_name='res.users', string="Seller", default=lambda self: self.env.user)
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string="Tags")
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string="")
    best_offer = fields.Float(compute='_compute_best_offer')
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer received"),
            ('offer_accepted', "Offer accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        default='new',
        copy=False,
    )

    _check_expected_price = models.Constraint('CHECK(expected_price > 0)', "The expected price must be stricly positive")

    _check_selling_price = models.Constraint('CHECK(selling_price > 0)', "The selling price must be stricly positive")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record_property in self:
            record_property.total_area = record_property.living_area + record_property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record_property in self:
            record_property.best_offer = max(record_property.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_expected_price(self):
        for record_property in self:
            if not float_is_zero(record_property.selling_price, precision_digits=2) and (
                float_compare(record_property.expected_price * 0.9, record_property.selling_price, precision_digits=2) > 0):
                raise UserError(self.env._("The selling price must be a least 90% of the expected price!"))

    def action_cancel(self):
        for record_property in self:
            if record_property.state == 'sold':
                raise UserError(record_property.env._("Sold properties cannot be cancelled"))
            record_property.state = 'cancelled'
        return True

    def action_sold(self):
        for record_property in self:
            if record_property.state == 'cancelled':
                raise UserError(record_property.env_("Canceled properties cannot be sold"))
            record_property.state = 'sold'
        return True

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        if any((property_id.state not in ('new', 'cancelled')) for property_id in self):
            raise UserError(self.env._("You can only delete property in the state New or Cancelled"))

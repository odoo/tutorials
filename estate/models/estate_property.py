# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"
    _order = 'id desc'

    _check_expected_price = models.Constraint('Check(expected_price > 0)', "The expected price must be strictly positive.")
    _check_selling_price = models.Constraint('Check(selling_price >= 0)', "The selling price must be positive.")

    name = fields.Char(required=True, string="Name")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        string="Garden Orientation",
    )
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default='new',
        required=True,
        string="Status",
    )
    buyer_id = fields.Many2one(comodel_name='res.partner', string="Buyer")
    salesperson_id = fields.Many2one(comodel_name='res.users', string="Salesperson", default=lambda self: self.env.user)
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string="Property Type")
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string="Tags")
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        string="Offers",
    )
    total_area = fields.Integer(compute='_compute_total_area', string="Total Area (sqm)")
    best_price = fields.Float(compute='_compute_best_price', string="Best Offer Price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            if property.offer_ids:
                property.best_price = max(property.offer_ids.mapped('price'))
            else:
                property.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            if not float_is_zero(property.selling_price, precision_digits=2):
                if float_compare(property.selling_price, property.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError(self.env._("The selling price cannot be lower than 90% of the expected price."))

    def action_sold(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError(self.env._("Cancelled property cannot be sold."))
            property.state = 'sold'
        return True

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError(self.env._("Sold property cannot be cancelled."))
            property.state = 'cancelled'
        return True

    @api.ondelete(at_uninstall=True)
    def delete(self):
        for property in self:
            if property.state not in ('new', 'cancelled'):
                raise UserError(self.env._("Only new and cancelled properties can be deleted."))
        return super().unlink()

from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)', "Expected price should be positive."
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)', "Selling price must be positive."
    )

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: date.today() + relativedelta(months=3))
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
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        string="Garden Orientation"
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
        string="Status",
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            prices = property.offer_ids.mapped('price')
            property.best_price = max(prices, default=0.0)

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for property in self:
            if not float_is_zero(property.selling_price, precision_digits=2) and (
                float_compare(
                    property.selling_price,
                    0.9 * property.expected_price,
                    precision_digits=2,
                )
                == -1
            ):
                raise ValidationError("Selling price must be at least 90% of the expected price.")

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _check_offers_before_delete(self):
        for property in self:
            if property.state not in ['new', 'cancelled']:
                raise UserError("Cannot delete a property that is currently active or sold.")

    def action_cancel_property(self):
        for property in self:
            if property.state == 'sold':
                raise UserError(self.env._("Sold properties cannot be cancelled."))
            property.state = 'cancelled'
        return True

    def action_sold_property(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            property.state = 'sold'
        return True

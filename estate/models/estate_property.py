from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.tools import float_compare
from odoo.exceptions import ValidationError, UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "All property created"
    _order = 'id desc'

    name = fields.Char(required=True, string="Title")
    description = fields.Text(string="Description")
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda p: fields.Date.today() + relativedelta(months=3), copy=False,
                                     string="Available Date")
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, copy=False, string="Selling price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    active = fields.Boolean(default=True)
    garden_area = fields.Integer(string="Garden Area", default=0)

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)

    tag_ids = fields.Many2many('estate.property.tag')

    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string="Offer")

    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")]
    )

    state = fields.Selection(
        string="Status",
        required=True,
        default='new',
        selection=[
            ('new', "New"),
            ('offer', "Offer"),
            ('received', "Offer Received"),
            ('accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
       ]
    )

    total_area = fields.Float(compute='_compute_total_area')

    best_price = fields.Float(compute='_compute_best_price')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        "The expected price must be strictly positive.",
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        "The selling price must be positive.",
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_sell_price(self):
        for estate in self:
            if len(estate.offer_ids) > 0 and float_compare(estate.selling_price, estate.expected_price * 0.9, 2) == -1:
                raise ValidationError(self.env._("Put a higher price"))
        return True

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.garden_area + estate.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for estate in self:
            prices = estate.offer_ids.filtered(lambda o: o.status != 'refused').mapped('price')
            estate.best_price = max(prices) if len(prices) > 0 else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 5 * self.garden
        self.garden_orientation = 'north' if self.garden else None

    def action_cancel_sell(self):
        for estate in self:
            if estate.state == 'sold':
                raise UserError(self.env._("Sold properties can not be canceled"))

            estate.state = 'cancelled'
        return True

    def action_sell(self):
        for estate in self:
            if estate.state == 'cancelled':
                raise UserError(self.env._("Cancelled properties can not be sell"))

            estate.state = 'sold'
        return True

    def set_received(self):
        for estate in self:
            estate.state = 'received'
        return True

    def accepted_offer(self, offer):
        for estate in self:
            if offer.status == 'accepted':
                estate.selling_price = offer.price
                estate.buyer_id = offer.partner_id
                estate.state = 'accepted'
        return True

    @api.model
    def ondelete(self):
        for property in self:
            if property.state != 'new' or property.state != 'cancelled':
                raise ValidationError(self.env._("Can only delete new or cancelled properties"))
        return super().ondelete()
    
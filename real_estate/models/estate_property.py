from datetime import date

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class Estate(models.Model):
    _name = 'estate.property'
    _description = "Real_Estate_Property"
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Date Availability",
        default=lambda self: date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    active = fields.Boolean(string="Active", default=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('offered', "Offer Received"),
            ('accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
    )
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ]
    )
    sales_person = fields.Many2one(
        'res.users',
        string="Sales Person",
        copy=False,
        default=lambda self: self.env.user,
    )
    buyer = fields.Many2one('res.partner', string="Buyer")
    property_type = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
    )
    tags = fields.Many2many('estate.property.tags', string="Tags")
    offer_ids = fields.One2many('estate.property.offers', 'property_id', string="Offers")
    total_area = fields.Integer(compute='_compute_total_area')
    best_offer = fields.Float(compute='_compute_best_offer')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            offers = record.offer_ids.mapped('price')
            if offers:
                record.best_offer = max(offers)
            else:
                record.best_offer = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = 0

    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._("This property cannot be sold."))
            record.state = 'sold'
        return True

    def action_set_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._("This property is sold."))
            record.state = 'cancelled'
        return True

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError(self.env._("Expected price cannot be negative."))

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError(self.env._("Selling price cannot be negative."))
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                raise ValidationError(self.env._("The selling price cannot be lower than 90% of the expected price!"))

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError(self.env._("This property cannot be deleted."))

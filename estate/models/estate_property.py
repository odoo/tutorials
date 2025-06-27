from datetime import date, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', "Expected price must be strictly positive."),
        ('check_selling_price', 'CHECK(selling_price >= 0)', "Selling price must be strictly positive.")
    ]

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facade")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        string="Garden Orientation"
    )
    available = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Received"),
            ('offer_accepted', "Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
            ('refused', "Refused")
        ],
        required=True,
        copy=False,
        default='new'
    )
    note = fields.Text(string="Special mention about the property.")
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped("price"))
            else:
                record.best_offer = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def cancel_property_button(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancelled'
            else:
                raise UserError("You cannot cancel a sold property.")

    def sold_property_button(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'sold'
            else:
                raise UserError("You cannot sell a cancelled property.")

    @api.constrains('expected_price')
    def _check_expected_price_positive(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("Expected price must be strictly positive.")

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_margin(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_acceptable_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_acceptable_price, precision_digits=2) < 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    def unlink(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("YOU CANNOT DELETE A PROPERTY THAT IS NOT IN NEW OR CANCELLED STATUS. REVERT!")
        return super().unlink()

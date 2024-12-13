from odoo import api, models, fields
from datetime import date,timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True, string="Name")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    available_from = fields.Date(string="Available From", default=date.today() + timedelta(days=90),copy=False)
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
            ],
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offered received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cnacelled', 'Cancelled')
            ],
        default='new',
        required=True
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    total_area = fields.Float(compute="_compute_total_area")
    status = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
            ],
        default='new',
        required=True
    )
    best_price = fields.Float(compute="_compute_best_offer")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'A property expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'A property Selling price must be positive'),
    ]

    @api.constrains('expected_price', 'selling_price')
    def _not_lower_than_ninty_percent(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            if float_compare(record.selling_price, record.expected_price*0.9, precision_rounding=0.01) == -1:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def sold_property(self):
        for record in self:
            if record.status == 'new':
                record.status = 'sold'
            elif record.status == 'canceled':
                raise UserError("A cancelled property cannot be sold")
        return True

    def cancel_property(self):
        for record in self:
            if record.status == 'new':
                record.status = 'canceled'
            elif record.status == 'sold':
                raise UserError("A sold property cannot be cancelled")
            return True

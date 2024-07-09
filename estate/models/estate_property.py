from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate properties defined"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(string="Status", selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], required=True, copy=False, default='new', readonly=True)
    active = fields.Boolean(string="Active", default=True)

    # Relationships
    # Many2One
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    sales_person = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)

    # Many2Many
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    # One2Many
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # compute functions fields and functions
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    best_price = fields.Integer(compute="_compute_max_price", string="Best Price")

    # sql constraints
    _sql_constraints = [('expected_price_positive', 'CHECK(expected_price > 0)', "The Expected Price cannot be negative"), ('selling_price_positive', 'CHECK(selling_price >= 0)', "The Selling Price cannot be negative")]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_max_price(self):
        for record in self:
            best_price = max(record.offer_ids.mapped("price"), default=0.0)
            record.best_price = best_price

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_estate_property_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancel Properties can't be Sold")
                return False
            else:
                record.state = 'sold'
                return True

    def action_estate_property_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold Properties can't be cancel")
                return False
            else:
                record.state = 'cancelled'
                return True

    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        decimal_precision = self.env['decimal.precision'].precision_get('Percentage Analytic')
        for record in self:
            if float_compare(record.selling_price, record.expected_price * 90.0 / 100.0, precision_digits=decimal_precision) < 0 and not float_is_zero(record.selling_price, precision_digits=decimal_precision):
                raise ValidationError("Selling price should be greater than 90 percent of the expected price")

from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Property Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(string='State', required=True, default='new', copy=False,
                             selection=[
                                 ('new', 'New'),
                                 ('offer_received', 'Offer Received'),
                                 ('offer_accepted', 'Offer Accepted'),
                                 ('sold', 'Sold'),
                                 ('cancelled', 'Canceled')
                             ]
                             )
    property_type_id = fields.Many2one("estate.property.type")
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price", string="Best offer")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for estate_property in self:
            estate_property.total_area = estate_property.garden_area + estate_property.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for estate_property in self:
            estate_property.best_price = max(estate_property.mapped('offer_ids.price')) if self.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False

    def action_property_sold(self):
        for estate_property in self:
            if estate_property.state == 'cancelled':
                raise UserError("Can't sell a cancelled property!")
            estate_property.state = 'sold'
        return True

    def action_property_cancelled(self):
        for estate_property in self:
            if estate_property.state == 'sold':
                raise UserError("Can't cancel a sold property!")
            estate_property.state = 'cancelled'
        return True

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for estate_property in self:
            if float_compare(estate_property.selling_price, estate_property.expected_price * 0.9, precision_digits=2) == -1:
                raise ValidationError("Selling price should be at least 90% of expected price.")

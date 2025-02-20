from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'model for the properties in our app'

    # selling prices for the properties should be at least 90% of the expected price
    PROPERTY_SELLING_PRICE_THRESHOLD = 0.9

    # epsilon to define the rounding precision when comparing floats
    PROPERTY_PRICE_PRECISION_EPSILON = 1e-6

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy = False,
        default = fields.Date.add(fields.Date.today(), months = 3)
    )
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = "Garden Orientation",
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        help = 'garden orientation is used to choose the orientation of the garden attached to the property'
    )
    active = fields.Boolean(default = True)
    state = fields.Selection(
        string = "State",
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default = 'new',
        required = True,
        copy = False,
    )
    property_type_id = fields.Many2one("estate.property.type", string = "Property Type")
    buyer_id = fields.Many2one("res.partner", string = "Buyer", copy = False)
    salesperson_id = fields.Many2one("res.users", string = "Salesperson", default = lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag", string = "Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string = "Offers")
    total_area = fields.Float(compute = "_compute_total_area")
    best_offer = fields.Float(compute = "_compute_best_offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default = 0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = ''
        else:
            self.garden_orientation = 'north'
            self.garden_area = 10

    def action_cancel_property(self):
        if self.filtered(lambda record: record.state == 'sold'):
            raise UserError('Sold properties cannot be cancelled')
        self.state = 'cancelled'
        return True

    def action_sell_property(self):
        if self.filtered(lambda record: record.state == 'cancelled'):
            raise UserError('Cancelled properties cannot be sold')
        self.state = 'sold'
        return True

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding = self.PROPERTY_PRICE_PRECISION_EPSILON):
                continue
            if float_compare(
                record.selling_price, record.expected_price * self.PROPERTY_SELLING_PRICE_THRESHOLD,
                precision_rounding = self.PROPERTY_PRICE_PRECISION_EPSILON
            ) < 0:
                raise UserError('The selling price must be at least 90% of the the expected price')

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be positive'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive'),
    ]

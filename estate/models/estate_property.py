from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Property Description', required=True)
    date_availability = fields.Date(string='Date Availability', copy=False,
                                    default=lambda self: fields.Date.today() + timedelta(days=3))
    postcode = fields.Char('Postal Code')
    selling_price = fields.Float('Selling Price', readonly=True, copy=False, default=0.00)
    expected_price = fields.Float('Expected Price', required=True)
    bedrooms = fields.Integer('No of. Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden Area(sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string='Garden Orientation',
    )
    total_area = fields.Integer(string='Total Area(sqm)', compute='_compute_total_area')
    sold = fields.Boolean('Sold', default=False)
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string='State',
        default='new',
        required=True,
        copy=False
    )
    property_type_id = fields.Many2one("estate.property.type", string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    best_price = fields.Float('Best Offer', compute='_compute_best_offer')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property must be positive',
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price of a property must be positive',
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_percentage(self):
        if (
                not float_is_zero(self.selling_price, precision_digits=2)
                and float_compare(self.selling_price, (self.expected_price * (90 / 100)), precision_digits=2) == -1
        ):
            raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.onchange("state")
    def _onchange_status(self):
        if self._origin.state == 'cancelled' and self.state == 'sold':
            raise ValidationError("This property has already been cancelled and cannot be sold.")
        elif self._origin.state == 'sold' and self.state == 'cancelled':
            raise ValidationError("This property has already been sold and cannot be cancelled.")

    def action_cancel_property(self):
        self.ensure_one()
        if self.state == 'sold':
            raise ValidationError("This property has already been sold and cannot be cancelled.")
        self.state = 'cancelled'

    def action_sold_property(self):
        self.ensure_one()
        if self.state == 'cancelled':
            raise ValidationError("This property has already been cancelled and cannot be sold.")
        self.state = 'sold'

from odoo import fields, models, api
from odoo.exceptions import ValidationError
import odoo
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char('Property Name', required=True, translate=True, default='Unknown')
    availability = fields.Date('Availability Date', required=True, default=lambda self: date.today() + relativedelta(months=3), copy=False)
    postcode = fields.Char('Postal Code', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    expected_price = fields.Float('Expected Price', default=0)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    living_area = fields.Integer('Living Area')
    bedrooms = fields.Integer('Bedrooms', help='number of bedrooms', default=2)
    facades = fields.Integer('Facades', help='number of facades')
    active = fields.Boolean('Active', default=True)
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offerreceived', 'Offer Received'), ('offeraccepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new',
    )
    property_type_id = fields.Many2one(
        string='Property Type',
        comodel_name='estate.property.type',
    )
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.users", string="Buyer", copy=False)
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        string='Offers',
        comodel_name='estate.property.offer',
        inverse_name='property_id'
    )
    total_area = fields.Integer(string='Total Area', compute='_compute_total_area')
    best_price = fields.Float(string='Highest Price', compute='_compute_highest_price')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'The expected price cannot be negative',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price cannot be negative',
    )

    @api.depends('offer_ids.price')
    def _compute_highest_price(self):
        prices = self.offer_ids.mapped('price')
        if prices:
            self.best_price = max(prices)
        else:
            self.best_price = 0

    @api.depends("living_area", 'garden_area')
    def _compute_total_area(self):
        self.total_area = self.living_area + self.garden_area

    @api.onchange("garden")
    def _inverse_validity(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False

    @api.constrains('selling_price', 'expected_price')
    def _check_price_percentage(self):
        for record in self:
            if record.selling_price <= record.expected_price * 0.9:
                raise ValidationError("The selling price must be at least 90% of the expected price")

    def action_sold(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'sold'
            else:
                odoo.exceptions.UserError('Cancelled properties cannot be sold')

    def action_cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancelled'
            else:
                odoo.exceptions.UserError('Sold properties cannot be cancelled')

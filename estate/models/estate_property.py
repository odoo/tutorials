# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = "sequence_number desc"

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price must be positive.'),
        ('unique_property_type', 'UNIQUE(name)',
         'Property name must be unique.')
    ]
    sequence_number = fields.Char(string="Number", copy=False, readonly=True, default="New")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
        required=True
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store=True)
    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Availability Date",
        default=lambda self: fields.Date.to_string(datetime.today() + timedelta(days=90)),
        copy=False
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Float(string="Total Area", compute="_compute_total_area")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string="State",
        required=True,
        copy=False,
        default='new'
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        """ Computes the total area as the sum of living_area and garden_area.
        This method is triggered when either of these fields is updated."""
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        """Computes the best (highest) offer price from the related offers.
        If there are no offers, defaults to 0.0."""
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price"), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sell_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be sold.")
            if not record.buyer_id or not record.selling_price:
                raise UserError("Property must have an accepted offer before being sold")
            record.state = "sold"

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled.")
            record.state = "cancelled"

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_valid_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_valid_price, precision_digits=2) == -1:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("sequence_number", "New") == "New":
                vals['sequence_number'] = self.env['ir.sequence'].next_by_code(
                    'estate.property')
        return super().create(vals_list)

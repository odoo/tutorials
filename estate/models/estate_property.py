from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property object"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3),
                                    string="Available from")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection([('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('cancelled', 'Cancelled')], default='new', copy=False, required=True, readonly=True, string="Status", store="True", compute="_compute_state")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.uid, string="Salesperson")
    buyer_id = fields.Many2one("res.partner", copy=False, string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _positive_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected Price must be positive',
    )

    _selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling Price must be positive',
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max((offer.price for offer in record.offer_ids if offer.status != 'refused'), default=0.0)

    @api.depends("offer_ids", "offer_ids.status")
    def _compute_state(self):
        for record in self:
            for offers in record.offer_ids:
                record.state = 'offer_received'
                if offers.status == 'accepted':
                    record.state = 'offer_accepted'
                    break

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            record.garden_area = 10 if record.garden else 0.0
            record.garden_orientation = 'north' if record.garden else None

    def action_sold_estate_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._("Cancelled property cannot be sold"))
            record.state = 'sold'

    def action_cancel_estate_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._("Sold property cannot be cancelled"))
            record.state = 'cancelled'

    @api.constrains('selling_price')
    def _constrains_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.001) and float_compare(record.selling_price, (0.9 * record.expected_price), precision_rounding=0.001) == -1:
                raise ValidationError(self.env._("The selling price cannot be lower than 90% of the expected price"))

    @api.constrains('expected_price')
    def _constrains_expected_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.001) and float_compare(record.selling_price, (0.9 * record.expected_price), precision_rounding=0.001) == -1:
                raise ValidationError(self.env._("The selling price cannot be lower than 90% of the expected price"))

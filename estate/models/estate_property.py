from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')],
        copy=False,
        required=True,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    property_offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive.'
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("property_offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.property_offer_ids:
                record.best_price = max(record.property_offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def sell_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(self.env._("Cancelled properties cannot be sold"))
            else:
                record.state = 'sold'
                return True

    def cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(self.env._("Sold properties cannot be cancelled"))
            else:
                record.state = 'cancelled'
                return True

    @api.constrains('selling_price', 'expected_price')
    def check_minimum_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2) and float_compare(record.selling_price, record.expected_price * 0.9, 2) < 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_cancelled(self):
        if any(record.state in ['offer_received', 'offer_accepted', 'sold'] for record in self):
            raise UserError(self.env._("Only new or cancelled properties can be deleted."))

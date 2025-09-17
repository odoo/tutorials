from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare


class Property(models.Model):
    _name = 'estate.property'
    _description = "Estate property"
    _order = 'id desc'

    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Number of Facades")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")])
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[
                                ('new', "New"),
                                ('offer_received', "Offer Received"),
                                ('offer_accepted', "Offer Accepted"),
                                ('sold', "Sold"),
                                ('cancelled', "Cancelled")
                            ], default='new', required=True, copy=False, string="Status")
    property_type_id = fields.Many2one('estate.property.type')
    salesman_id = fields.Many2one('res.users')
    buyer_id = fields.Many2one('res.partner')
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float("Best Offer", compute='_compute_best_price')

    _check_expected_price_positive = models.Constraint('CHECK(expected_price >= 0)', "The expected price must be positive.")
    _check_selling_price_positive = models.Constraint('CHECK(selling_price >= 0)', "The selling price must be positive.")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and float_compare(record.selling_price, (0.9 * record.expected_price), 2) < 0:
                raise ValidationError("The selling price must be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError("Only new and cancelled properties can be deleted.")

    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cannot sell a cancelled property")

            record.state = 'sold'
        return True

    def action_set_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Cannot cancel a sold property")
            record.state = 'cancelled'
        return True

from datetime import date, timedelta
from odoo import api, models, fields, exceptions, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    # _inherit = "estate.property"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: date.today() + timedelta(days=90), copy=False)
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], default='new', required=True, copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user, required=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", store=True)
    best_offer = fields.Float(compute="_compute_best_offer", store=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("A sold property cannot be cancelled!")
            record.state = 'cancelled'

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("A cancelled property cannot be sold!")
            if record.best_offer == 0.0:
                raise exceptions.UserError("No offers available to sell the property.")
            record.state = 'sold'
            record.selling_price = record.best_offer

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, 0, precision_rounding=0.01) > 0:  # Selling price is not zero
                minimum_price = record.expected_price * 0.9
                if float_compare(record.selling_price, minimum_price, precision_rounding=0.01) < 0:
                    raise ValidationError(
                        "The selling price cannot be lower than 90% of the expected price."
                    )
    @api.ondelete(at_uninstall=False)
    def _check_state_on_delete(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(_("You can only delete properties in the 'New' or 'Cancelled' state."))

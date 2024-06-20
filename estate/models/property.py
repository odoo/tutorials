# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils

class Property(models.Model):
    _name = "property"
    _description = "Properties of the Real Estate"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text(required=True)
    postcode = fields.Char()
    date_availability = fields.Date(string = "Available from",copy = False, default = fields.Date.add(fields.Datetime.today() + relativedelta(months=3)))
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default = lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy = False)
    offer_ids = fields.One2many("property.offer", "property_id", "Offers")
    expected_price = fields.Float()
    best_price = fields.Float(compute = '_compute_best_price')
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'),('east', 'East'),('west', 'West')],
        help="Type is used to set the orientation")
    garden_area = fields.Float()
    living_area = fields.Float(string = "Living Area (sqm)")
    total_area = fields.Float(compute = '_compute_total_area')
    active = fields.Boolean(default = True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')],
        required=True,
        copy = False,
        default = 'new')
    property_type_id = fields.Many2one("property.type", string="Property Type")
    tag_ids = fields.Many2many("property.tag", string="Tags")

    _sql_constraints  = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Odoopsie! The expected price must be positive' ),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Odoopsie! The selling price must be positive' )
    ]

    @api.depends("living_area","garden_area")
    def _compute_total_area(self) :
        for real_estate in self :
            real_estate.total_area = real_estate.living_area + real_estate.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self) :
        for real_estate in self :
            if len(real_estate.offer_ids) == 0 : real_estate.best_price = 0
            else : real_estate.best_price = max([offer.price for offer in real_estate.offer_ids])

    @api.onchange("garden")
    def _onchange_garden(self) :
        """ This function is triggered when the user chooses to use a garden or not"""
        if self.garden :
            self.garden_area = 10
            self.garden_orientation = "north"
        else :
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains('selling_price')
    def _check_selling_price(self) :
        for real_estate in self :
            if float_utils.float_compare(self.selling_price, 0.9 * self.expected_price, 2) == -1 :
                raise ValidationError("The price must be at least 90 percent of the expected price")

    def action_set_state_sold(self):
        for real_estate in self:
            if real_estate.state == "cancelled" : raise UserError(_('The property is already cancelled, so it cannot be sold LOL'))
            else : real_estate.state = "sold"
        return True
    
    def action_set_state_cancelled(self):
        for real_estate in self:
            if real_estate.state == "sold" : raise UserError(_('The property is already sold, so it cannot be cancelled LOL'))
            else : real_estate.state = "cancelled"
        return True

    @api.ondelete(at_uninstall = False)
    def _unlink_according_to_state(self) :
        """Unlinks the property only if it is in state new or cancelled"""
        for real_estate in self :
            if real_estate.state != 'new' and real_estate.state != 'cancelled' :
                raise UserError("Odoopsie! Can't delete a property which status isn't New or Cancelled")
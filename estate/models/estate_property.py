# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _inherit = ["mail.thread"]
    _order = "id desc"
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The selling price must be positive"),
    ]

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=lambda self: fields.Date.context_today(self) + relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )

    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        selection = [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        string="Status", required=True, default="new", copy=False, tracking=True,
        help='New: A new property with no offers yet\n'
            'Offer Received: Offers by buyers are received\n'
            'Offer Accepted: An offer has been accepted\n'
            'Sold: property is sold\n'
            'Cancelled: property cancelled')

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.company)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float("Best Offer", compute="_compute_best_price", help="Best offer received")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price")) if property.offer_ids else 0.0

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for property in self:
            if (property.selling_price != 0
                and float_compare(property.selling_price, property.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0):
                raise ValidationError(_("The selling price cannot be lower than 90% of the expected price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        if any(property.state not in ("new", "cancelled") for property in self):
            raise UserError(_('You cannot delete a property which is not new or cancelled.'))

    def action_sold(self):
        if "cancelled" in self.mapped("state"):
            raise UserError(_("Cancelled properties cannot be sold."))
        # This condition ensures that buyer and selling price are set before marking property sold
        if self.mapped("state").count("offer_accepted") != len(self):
            raise UserError(_("Cannot sell a property with no accepted offer."))
        for property in self:
            property.state = "sold"
        return True

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError(_("Sold properties cannot be cancelled."))
        for property in self:
            property.state = "cancelled"
        return True

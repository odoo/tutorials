# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import math
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _sql_constraints = [
        ('check_positive_values_expected_price', 'CHECK(expected_price>0)',
         'Expected price must be positive'),
         ('check_positive_values_selling_price', 'CHECK(selling_price>0)',
         'Selling price must be positive')
    ]

    name = fields.Char(string="Property Name", required=True, default="Unknown name")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Condition") # all many2many fields have suffix _ids.
    property_type_id = fields.Many2one("estate.property.type", string="Property Type" ) # all many2one field have suffix _id, and it display by default name of estate.property.type
    salesmen_id = fields.Many2one("res.users", string="Salesmen", default=lambda self: self.env.user) # many2one field by default display name field of other model, self.env.user return current user's name
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    company_id = fields.Many2one("res.company",string="Company", required=True, default=lambda self: self.env.company)
    active=fields.Boolean(default=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Has Garage?")
    garden = fields.Boolean(string="Has Garden?")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    best_offer = fields.Float(compute="_compute_best_price", string="Best Offer")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled','Cancelled')
        ],
        string="state", default="new",
        copy=False, required=True
    )
 

    @api.depends("living_area", "garden_area")  # this method call when living_area or garden_area change.
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        maxprice = 0
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold_property(self): # method for sold button
        for record in self:
            if record.state == "cancelled":
                  raise UserError("Cancelled Property cannot be sold")
            else:
                record.state = "sold"
        return True

    def action_cancel_property(self): # method for cancel button
        for record in self:
            if record.state == "sold":
                raise UserError("Sold Property cannot be cancel")
            else:
                record.state = "cancelled"
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_minimum_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.9:
                raise ValidationError("Selling price should be greater than 90% of expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_is_new_or_cancelled(self):
        for record in self:
            if record.state!='new' and record.state!='cancelled':
                raise UserError('You cannot delete a property which is not new or cancelled.')

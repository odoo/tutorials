# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Name", required=False, copy=False)
    description = fields.Text(copy=True)
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=lambda self:fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean("active", default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold_cancelled", "Sold and Cancelled"),
            ("cancel", "Cancel")
        ]
    )
    property_type_id = fields.Char(string="Property id")
    salesman_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Partner", copy=False)
    tag_ids=fields.Many2many('estate.property.tag', "estate_property_estate_property_tag_rel", "estate_property_id", "estate_property_tag_id")
    type_ids=fields.Many2many('estate.property.type', 'estate_property_estate_property_type_rel', 'estate_propety_id', 'estate_property_type_id')
    offer_ids=fields.One2many("estate.property.offer", "property_id", string="offerid")
    total_area=fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    
    _sql_constraints=[
            ("check_expected_price", "CHECK(expected_price >= 0)", "Price should be positive"),
            ("check_selling_price", "CHECK(selling_price >= 0)", "Selling price should be positive")
    ]
    
    @api.depends("garden_area", "garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area=rec.garden_area + rec.living_area
         
    @api.onchange("garden")
    def _onchange_garden(self):
        if (self.garden == True):
             self.garden_orientation="north"
             self.garden_area=10  
        else:
            self.garden_orientation=""
            self.garden_area=0     
           
    def action_sold(self):
        for rec in self:
            if(rec.state != "cancel"):
                 rec.state="sold_cancelled"
            else:
                raise UserError("Canceld property can not be sold")
                           
    def action_cancel(self):
        for rec in self:
            if(rec.state != "sold_cancelled"):
                rec.state="cancel"
            else:
                raise UserError("Sold property can not be cancel")

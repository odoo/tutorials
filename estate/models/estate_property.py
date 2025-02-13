# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id asc"

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
            ("sold", "Sold"),
            ("cancel", "Cancel")
        ],
    default='new')
    salesman_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Partner", copy=False)
    tag_ids=fields.Many2many('estate.property.tag', "estate_property_estate_property_tag_rel", "estate_property_id", "estate_property_tag_id")
    property_type_id=fields.Many2one('estate.property.type', string="Property Type")
    offer_ids=fields.One2many("estate.property.offer", "property_id", string="offerid")
    total_area=fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    best_price=fields.Float(compute='_compute_best_price', string="Best Offer")
    
    _sql_constraints=[
            ("check_expected_price", "CHECK(expected_price >= 0)", "Price should be positive"),
            ("check_selling_price", "CHECK(selling_price >= 0)", "Selling price should be positive")
    ]    
        
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for rec in self:
            rec.best_price=max([line.price for line in rec.offer_ids], default=0)
    
    @api.depends("living_area", "garden_area")
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
                 rec.state="sold"
            else:
                raise UserError(_("Canceled property can not be sold"))
                           
    def action_cancel(self):
        for rec in self:
            if(rec.state != "sold"):
                rec.state="cancel"
            else:
                raise UserError(_("Sold property can not be cancel"))

    @api.ondelete(at_uninstall=False)
    def _prevent_deletion(self):
        for rec in self:
            if(rec.state not in ['new', 'canceled']):
                raise UserError(_("Can't delete  this property!" ))

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    
    price=fields.Float(string="Price")
    status=fields.Selection(
                  selection=[
                        ("accepted", "Accepted"),
                        ("refused", "Refused")
                        ],
                  string="status", copy=False)
    partner_id=fields.Many2one("res.partner", string="Partner", required=True)
    property_id=fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", related="property_id.property_type_id", store=True)
    validity=fields.Integer(string="Validity")
    date_deadline=fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", default=lambda self:fields.Date.today())
    
    _sql_constraints=[
            ("check_price", "CHECK(price >= 0)", "Price should be positive")
    ]
    
    @api.depends("validity")
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline=(rec.create_date  or fields.Date.today()) + relativedelta(days = rec.validity)
    
    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity=(rec.date_deadline - fields.Date.today()).days or 0       
    
    def action_accepted(self):
            self.status="accepted"
            self.property_id.selling_price = self.price
            self.property_id.partner_id = self.partner_id
            self.property_id.status="offer_accepted"
            
    def action_refused(self):
            self.status="refused"   
       
    @api.constrains('price')        
    def _check_price(self):
            for rec in self:
                    if(rec.price < (rec.property_id.expected_price * 90) / 100):
                           raise UserError(_(r"Selling price cannot be less than 90% of the expected price."))


    @api.model_create_multi
    def create(self, rec_list):
            for rec in rec_list:
                    if rec["property_id"]:
                            val = self.env["estate.property"].browse(rec["property_id"])
                    if val.status == 'sold':
                            raise UserError("property is already sold")
                    if rec["price"] < val.best_price:
                            raise UserError("price must be greater than best price")  
                    if val.status == "new":
                            val.status = "offer_received"      
            return super().create(rec_list)       

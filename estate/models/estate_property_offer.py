# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Eastate Property Offer"
    
    price=fields.Float(string="Price")
    status=fields.Selection(
                  selection=[
                        ("accepted", "Accepted"),
                        ("refused", "Refused")
                        ],
                  string="status", copy=False)
    partner_id=fields.Many2one("res.partner", string="Partner", required=True)
    property_id=fields.Many2one("estate.property", string="Property", required=True)
    validity=fields.Integer("Validity")
    date_deadline=fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
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
            
    def action_refused(self):
            self.status="refused"   

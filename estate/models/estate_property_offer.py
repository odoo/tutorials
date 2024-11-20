# -*- coding: utf-8 -*-
# licence

from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offers"
    # _order = "sequence"

    name = fields.Char('Name', required=False, default="- no name -")
    price = fields.Float('Offer price', required=True)
    validity = fields.Integer('Validity time')
    # Reserved
    state = fields.Selection(string="Status", selection=[('new', 'New'), ('accepted', 'Accepted'), ('refused', 'Refused')], default='new', required=True)
    # Relational
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    # Computed
    date_deadline = fields.Date("Deadline date", compute='_compute_deadline', inverse='_inverse_deadline')
    
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date.date(), days=record.validity)
            
    def _inverse_deadline(self):
        for record in self:
            record.validity = (fields.Date.delta(record.create_date.date(), record.date_deadline)).days
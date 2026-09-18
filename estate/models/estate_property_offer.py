# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offers for the estate"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
        readonly=True,
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    partner_id = fields.Many2one("res.partner", copy=False)
    property_id = fields.Many2one("estate.property", string="Property", copy=False)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(start_date, days=record.validity)
    
    @api.depends("date_deadline", "create_date")
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            for other_offer in record.property_id.offer_ids:
                if other_offer.status == "accepted" :
                    other_offer.status = False
                    Warning("An other offer acceptation was cancelled : only one offer can be accepted at a time !")
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id._update_state_from_offers()
        return True
    
    def action_reset(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.buyer_id = False
                record.property_id.selling_price = 0
            record.status = False
            record.property_id._update_state_from_offers()
        return True
    
    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.buyer_id = False
                record.property_id.selling_price = 0
            record.status = "refused"
            record.property_id._update_state_from_offers()
        return True

    _positive_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer prices should be strictly positive.',
    )


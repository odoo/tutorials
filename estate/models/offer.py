import logging
from datetime import datetime
from odoo.exceptions import UserError
from odoo import fields, models, api
from odoo.tools import add,subtract

class Offer(models.Model):
    _name = "offer"
    _description = "Offer"
    price = fields.Float(string="Price")
    status = fields.Selection(copy=False, string="Status", selection=[ ("accepted", "Accepted"), ("refused", "Refused")],
                              required=True)
    partner_id = fields.Many2one("res.partner", string="Partner",required=True)
    property_id = fields.Many2one("estate_property", string="Estate Property",required=True)
    validity= fields.Integer(string="Validity",default="7")
    date_deadline = fields.Date(string="Date Deadline",inverse="_inverse_total",compute="_compute_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline=add(record.create_date if record.create_date else fields.Date.today(), days=record.validity)

    def _inverse_total(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def accept(self):
        for record in self:
            for i in record.property_id.offer_ids:
                if i.status=="accepted":
                    raise UserError("An offer was already accepted")
            record.status="accepted"
        return True

    def refuse(self):
        for record in self:
            record.status="refused"
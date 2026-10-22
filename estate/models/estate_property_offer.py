# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate offers tag info"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])
    validity = fields.Integer(string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity", "property_id.date_availability")
    def _compute_date_deadline(self):
        for record in self:
            if record.validity and record.property_id.date_availability:
                record.date_deadline = fields.Date.add(record.property_id.date_availability, days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.property_id.date_availability:
                record.validity = fields.Date.subtract(record.date_deadline, record.property_id.date_availability).day


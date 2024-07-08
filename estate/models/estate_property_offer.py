from odoo import models, fields, api
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                current_date = fields.Date.today()
                expiration_date = current_date + timedelta(days=record.validity)
                record.date_deadline = expiration_date
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                current_date = fields.Date.today()
                validity_days = (record.date_deadline - current_date).days
                record.validity = validity_days
            else:
                record.validity = 0

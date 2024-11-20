from odoo import models, fields, api
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Estate Property Offer"

    price=fields.Float("Price")
    status=fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    property_id = fields.Many2one('estate.property', 'Property', required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            td = record.date_deadline - record.create_date.date()
            record.validity = td.days
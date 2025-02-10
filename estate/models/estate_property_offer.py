from odoo import models,fields, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Real Estate Property Offer Model"

    price=fields.Float(required=True)
    status=fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id=fields.Many2one('res.partner',required=True, string="Partner")
    create_date = fields.Date(default=fields.Date.today)
    property_id=fields.Many2one('estate.property',required=True)
    validity = fields.Integer(default = 7, string = "Validity (days)")
    date_deadline = fields.Date(string="Deadline", compute = "_compute_date_deadline", inverse="_inverse_date_deadline", store = True)

    @api.depends("create_date","validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date
                record.validity = delta.days

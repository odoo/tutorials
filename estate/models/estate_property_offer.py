from odoo import models, fields, api
from datetime import date
from datetime import timedelta


class estate_property_offer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property offer"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_validity", string="Deadline")

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            today = record.create_date
            if today:
                today = record.create_date
            else:
                today = date.today()
            if record.date_deadline:
                record.date_deadline = today + (record.validity - (record.date_deadline - today).days)
            else:
                record.date_deadline = timedelta(days=record.validity) + today

    def _inverse_validity(self):
        for record in self:
            today1 = fields.Date.from_string(record.create_date)
            updated_deadline_date = fields.Date.from_string(record.date_deadline)
            record.validity = (updated_deadline_date - today1).days

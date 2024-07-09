from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property.offer"
    _description = "Real_Estate property model"

    price = fields.Float('Price', required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.partner_id = ""
                record.property_id.selling_price = 0.0
            record.status = "refused"

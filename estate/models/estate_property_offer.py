from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('pending', 'Pending'), ('accepted', 'Accepted'), ('refused', 'Refused')], required=True, default="pending")
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Datetime.now()
            record.date_deadline = fields.Date.add(base_date.date(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = (record.create_date or fields.Datetime.now()).date()
            deadline_date = record.date_deadline or base_date
            record.validity = (deadline_date - base_date).days

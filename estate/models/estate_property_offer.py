from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer made by a potential buyer"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Datetime(compute="_compute_deadline", inverse="_inverse_deadline")

    # Compute methods

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    # Action methods
    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            return True

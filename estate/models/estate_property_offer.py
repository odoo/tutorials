from dateutil.relativedelta import relativedelta
from odoo import fields, models, api


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offre d'achat"

    price = fields.Float("price")
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)
    date_deadline = fields.Date(default=fields.Date.today() + relativedelta(days=7), compute="_compute_deadline", inverse="_update_validity")
    validity = fields.Integer(default=7)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                now = record.create_date
                record.date_deadline = now + relativedelta(days=record.validity)

    def _update_validity(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days

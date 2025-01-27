from odoo import api, fields, models

class offer(models.Model):
    _name = 'estate.house_offer'

    price = fields.Float()
    status = fields.Selection(selection=[('Accepted','Accepted'),('Refused','Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', stirng='Partner', required=True)
    property_id = fields.Many2one('house', 'Property applied on', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_offer_deadline", inverse="_inverse_offer_deadline")

    @api.depends("validity")
    def _compute_offer_deadline(self):
        for offer in self:
            current_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(current_date, days=offer.validity)

    def _inverse_offer_deadline(self):
        for offer in self:
            current_date = fields.Date.to_date(offer.create_date or fields.Date.today())
            offer.validity = (offer.date_deadline - current_date).days
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    crm_lead_id = fields.Many2one('crm.lead', string='CRM Lead', copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            lead = self.env['crm.lead'].create({
                'name': f"Offer: {record.property_id.name}",
                'expected_revenue': record.price,
                'type': 'opportunity',
                'user_id': record.property_id.seller_id.id,
                'partner_id': record.partner_id.id,
            })
            record.crm_lead_id = lead
        return records

    def action_accept_offer(self):
        res = super().action_accept_offer()
        for offer in self:
            if offer.crm_lead_id:
                offer.crm_lead_id.action_set_won()
        return res

    def action_refuse_offer(self):
        res = super().action_refuse_offer()
        for offer in self:
            if offer.crm_lead_id:
                offer.crm_lead_id.action_set_lost()
        return res

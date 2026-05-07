from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    crm_lead_id = fields.Many2one('crm.lead', string='CRM Lead', copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            lead = self.env["crm.lead"].create({
                "name": record.property_id.name,
                "expected_revenue": record.price,
                "partner_id": record.partner_id.id,
            })
            record.crm_lead_id = lead
        return records

    def action_accept(self):
        res = super().action_accept()
        for offer in self:
            if offer.crm_lead_id:
                offer.crm_lead_id.action_set_won()
        for offer in self:
            other_offers = offer.property_id.offer_ids - offer
            other_offers.action_refuse()
        return res

    def action_refuse(self):
        res = super().action_refuse()
        for offer in self:
            if offer.crm_lead_id:
                offer.crm_lead_id.action_set_lost()
        return res

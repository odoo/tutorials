from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    lead_id = fields.Many2one(
        "crm.lead",
        string="CRM Lead",
        readonly=True,
        copy=False
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            lead = self.env["crm.lead"].create({
                "name": record.property_id.name,
                "partner_id": record.partner_id.id,
                "expected_revenue": record.price,
            })
            record.lead_id = lead.id
        return records

    def action_accept(self):
        result = super().action_accept()
        for offer in self:
            if offer.lead_id:
                offer.lead_id.action_set_won()
        for offer in self.property_id.offer_ids:
            if offer.id != self.id:
                offer.action_refuse()
        return result

    def action_refuse(self):
        result = super().action_refuse()
        for offer in self:
            if offer.lead_id:
                offer.lead_id.action_set_lost()
        return result

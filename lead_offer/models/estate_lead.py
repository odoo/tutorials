from odoo import models, fields


class EstateLead(models.Model):
    _inherit = "estate.property.offer"

    lead_id = fields.Many2one(
        "crm.lead",
        ondelete='cascade',
    )

    def create(self, vals_list):
        offer = super().create(vals_list)
        lead = self.env["crm.lead"].create({
            "partner_id": offer.partner_id.id,
            "name": offer.id,
            "expected_revenue": offer.price,
            "type": "opportunity",
        })
        offer.lead_id = lead.id
        return offer

    def action_accept(self):
        res = super().action_accept()
        for offer in self:
            if offer.lead_id:
                offer.lead_id.action_set_won()
        return res

    def action_refuse(self):
        res = super().action_refuse()
        for offer in self:
            if offer.lead_id:
                offer.lead_id.action_set_lost()
        return res

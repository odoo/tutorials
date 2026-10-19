from odoo import models, api, fields


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    lead_id = fields.Many2one("crm.lead", string="Lead", readonly=True, copy=False)

    @api.model
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            lead = self.env["crm.lead"].create(
                {
                    "name": offer.partner_id.name,
                    "type": "opportunity",
                    "date_deadline": offer.date_deadline,
                    "expected_revenue": offer.price,
                }
            )
            offer.lead_id = lead.id
        return offers

    def write(self, vals):
        result = super().write(vals)

        if "status" in vals:
            for offer in self:
                if not offer.lead_id:
                    continue

                if offer.status == "accepted":
                    stage = self.env["crm.stage"].search(
                        [("is_won", "=", True)], limit=1
                    )
                    if stage:
                        offer.lead_id.write({"stage_id": stage.id})

                elif offer.status == "refused":
                    offer.lead_id.action_set_lost()

        return result

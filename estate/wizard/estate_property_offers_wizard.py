from odoo import models, fields, api


class PropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Bulk Offer Creator"

    price = fields.Float("Offer Price", required=True)
    partner_id = fields.Many2one("res.partner", "Buyer", required=True)

    def action_create_offers(self):
        self.ensure_one()
        Offer = self.env["estate.property.offer"]
        properties = self.env.context.get("active_ids", [])

        Offer.create(
            [
                {
                    "price": self.price,
                    "partner_id": self.partner_id.id,
                    "property_id": pid,
                }
                for pid in properties
            ]
        )

        return {"type": "ir.actions.act_window_close"}
        

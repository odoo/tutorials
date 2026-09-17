from odoo import fields, models


class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Estate Property Offer Wizard"
    _transient_max_hours = 0.008333

    offer_id = fields.Many2one("estate.property.offer", required=True)

    def action_keep_previous(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window_close",
        }

    def action_accept_new(self):
        self.ensure_one()

        old_offer = self.env["estate.property.offer"].search(
            [
                ("property_id", "=", self.offer_id.property_id.id),
                ("status", "=", "accepted"),
                ("id", "!=", self.offer_id.id),
            ],
            limit=1,
        )

        old_offer.status = "refused"

        self.offer_id.status = "accepted"

        self.offer_id.property_id.selling_price = self.offer_id.price
        self.offer_id.property_id.buyer_id = self.offer_id.partner_id

        return {
            "type": "ir.actions.act_window_close",
        }

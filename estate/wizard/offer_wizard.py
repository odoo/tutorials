from odoo import fields, models


class OfferWizard(models.TransientModel):
    _name = "estate.offer.wizard"
    _description = "use for offer page"

    offer_id = fields.Many2one(
        "estate.property.offer",
    )

    def action_wizard_accept_offer(self):
        self.ensure_one()
        return self.offer_id.accept_offer()

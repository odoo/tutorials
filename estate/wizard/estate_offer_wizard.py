from odoo import api, fields, models


class EstateOfferWizard(models.TransientModel):
    _name = "offer.wizard"
    _description = "Wizard for offers"

    offer_price = fields.Float(string="Offer Price")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    @api.model_create_multi
    def create(self, vals):
        wizards = super().create(vals)
        for wizard in wizards:
            wizard._action_create_offers()
        return wizards

    def _action_create_offers(self):
        for wizard in self:
            properties = self.env["estate.property"].search(
                [
                    ("expected_price", "<=", wizard.offer_price),
                    ("state", "in", ("new", "offer_received")),
                    ("best_offer", "<", wizard.offer_price),
                    ("property_type_id", "=", wizard.property_type_id.id),
                ],
            )
            vals_list = [
                {
                    "property_id": property.id,
                    "price": wizard.offer_price,
                    "partner_id": wizard.partner_id.id,
                }
                for property in properties
            ]
            self.env["estate.property.offer"].create(vals_list)

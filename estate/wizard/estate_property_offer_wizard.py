from odoo import models, fields


class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Estate Property Offer Wizard"

    price = fields.Float("Offer Price", required=True)
    validity = fields.Integer("Validity", required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer", required=True)

    def make_offer(self):
        property_ids = self.env.context.get("active_ids", [])
        for property in property_ids:
            self.env["estate.property.offer"].create(
                {
                    "property_id": property,
                    "price": self.price,
                    "validity": self.validity,
                    "partner_id": self.buyer_id.id,
                }
            )
        return {"type": "ir.actions.act_window_close"}

from odoo import models, fields, api


class EstatePropertyMakeOffer(models.TransientModel):
    _name = "estate.property.make.offer"
    _description = "Estate Property Make Offer Wizard"

    property_ids = fields.Many2many("estate.property", string="Properties")
    offer_price = fields.Float(string="Offer Price")
    offer_validity = fields.Integer(string="Offer Validity")
    partner_id = fields.Many2one("res.partner", string="Partner")

    def make_offer(self):
        offers = []
        for property in self.property_ids:
            offer = self.env["estate.property.offer"].create(
                {
                    "price": self.offer_price,
                    "property_id": property.id,
                    "partner_id": self.partner_id.id,
                    "validity": self.offer_validity,
                }
            )
            offers.append(offer)

        if offers:
            return {
                "type": "ir.actions.act_window",
                "name": "Offer",
                "res_model": "estate.property.offer",
                "res_id": offers[-1].id, 
                "view_mode": "form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "type": "danger",
                    "message": "No offers were created.",
                },
            }

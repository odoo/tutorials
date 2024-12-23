from odoo import models, fields, api


class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Wizard for Adding Offer to Properties"

    price = fields.Float("Price")
    validity = fields.Integer("Validity")
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_ids = fields.Many2many("estate.property", string="Property")

    def action_make_offer(self):
        for property in self.property_ids:
            try:
                if property.id:
                    self.env["estate.property.offer"].create(
                        {
                            "price": self.price,
                            "validity": self.validity,
                            "property_id": property.id,
                            "partner_id": self.partner_id.id,
                        }
                    )
                property.write({"state": "offer_received"})

            except :
                print("Cannot add this offer to this property")

        return {"type": "ir.actions.act_window_close"}

    def action_cancel(self):
        return {"type": "ir.actions.act_window_close"}

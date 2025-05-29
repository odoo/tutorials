from odoo import api, fields, models


class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Property Offer Wizard"

    offer_price = fields.Float(string="Offer Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_ids = fields.Many2many("estate.property", string="Properties")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        property_ids = self.env.context.get("active_ids", [])
        if property_ids:
            res["property_ids"] = [(6, 0, property_ids)]
        return res

    def action_make_offer(self):
        for property_id in self.property_ids:
            self.env["estate.property.offer"].create(
                {
                    "offer_price": self.offer_price,
                    "partner_id": self.partner_id.id,
                    "property_id": property_id.id,
                }
            )
        return {"type": "ir.actions.act_window_close"}

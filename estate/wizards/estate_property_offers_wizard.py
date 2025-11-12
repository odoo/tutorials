from odoo import models, fields


class PropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offers.wizard"
    _description = "wizard to add multiple offers"

    price = fields.Float(required=True)
    partner_id = fields.Many2one("res.partner")
    validity = fields.Integer(default=7)

    def action_add_offers(self):
        property_ids = self.env.context.get("active_ids", [])
        
        offer_vals_list = []
        for property_id in property_ids:
            offer_vals = {
                "property_id": property_id,
                "price": self.price,
                "partner_id": self.partner_id.id,
                "validity": self.validity,
            }
            offer_vals_list.append(offer_vals)
        # print(offer_vals_list)
        # print("**" * 100)

        if len(offer_vals_list) > 0:
            self.env["estate.property.offers"].create(offer_vals_list)

        return {"type": "ir.actions.act_window_close"}

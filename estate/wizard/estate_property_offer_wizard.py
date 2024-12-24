from odoo import fields, models


class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Estate Property Offer Wizard"

    price = fields.Float(required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    partner_id = fields.Many2one("res.partner", required=True)

    def add_offers(self):
        property_ids = self.env.context.get("default_property_ids", [])
        for property_id in property_ids:
            self.env["estate.property.offer"].create(
                {
                    "price": self.price,
                    "validity": self.validity,
                    "partner_id": self.partner_id.id,
                    "property_id": property_id,
                }
            )
        return {"type": "ir.actions.act_window_close"}

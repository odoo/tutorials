from odoo import models, fields


class EstatePropertyMakeOffer(models.TransientModel):
    _name = "estate.property.make.offer"
    _description = "Estate Property Make Offer Wizard"

    property_ids = fields.Many2many("estate.property", string="Properties")
    offer_price = fields.Float(string="Offer Price")
    offer_validity = fields.Integer(string="Offer Validity")
    partner_id = fields.Many2one("res.partner", string="Partner")

    def make_offer(self):
        failed_properties = []
        for property in self.property_ids:
            try:
                self.env["estate.property.offer"].create(
                    {
                        "price": self.offer_price,
                        "property_id": property.id,
                        "partner_id": self.partner_id.id,
                        "validity": self.offer_validity,
                    }
                )
            except Exception:
                failed_properties.append(property.name)
        if failed_properties:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "message": "Failed to create offers for the following properties: "
                    + ", ".join(failed_properties),
                    "type": "danger",
                    "next": {"type": "ir.actions.act_window_close"},
                },
            }
        return {"type": "ir.actions.act_window_close"}

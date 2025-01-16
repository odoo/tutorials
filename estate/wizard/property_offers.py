from odoo import api, fields, models


class ProperyOffers(models.TransientModel):
    _name = "propery.offers"
    _description = "TransientModelmodel for offers"

    price = fields.Float("price", required=True)
    property_ids = fields.Many2many("estate.property", string="property_id")
    buyer_id = fields.Many2one("res.partner", required=True)
    validity = fields.Integer(default=7)

    def make_offer(self):
        failed_properties = []
        for property in self.property_ids:
            try:
                self.env["estate.property.offer"].create(
                    {
                        "price": self.price,
                        "property_id": property.id,
                        "buyer_id": self.buyer_id.id,
                        "validity": self.validity,
                    }
                )
            except Exception as e:
                print(f"{e} exception in ", property.name)
                failed_properties.append(str(e) + " in " + property.name)
        if failed_properties:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "message": " ".join(failed_properties),
                    "type": "danger",
                    "next": {"type": "ir.actions.act_window_close"},
                },
            }
        return {"type": "ir.actions.act_window_close"}

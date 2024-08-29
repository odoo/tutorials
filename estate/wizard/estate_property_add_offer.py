from odoo import fields, models


class AddOffer(models.TransientModel):
    _name = "add.offer"
    _description = "Add Offer in mutiple property"
    price = fields.Float()
    validity = fields.Integer(default=7)
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )

    def add_offer(self):
        context = self.env.context
        active_ids = context.get("active_ids", [])
        for recod in active_ids:
            self.env["estate.property.offer"].create(
                {
                    "property_id": recod,
                    "price": self.price,
                    "validity": self.validity,
                    "partner_id": self.buyer_id.id,
                }
            )

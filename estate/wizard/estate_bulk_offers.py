from odoo import fields, models


class EstateBulkOffers(models.TransientModel):
    _name = "estate.bulk.offers"
    _description = "Bulk Offers"

    price = fields.Float(string="Offer Price")
    validity = fields.Integer(default=7, string="Validity (days)")
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

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

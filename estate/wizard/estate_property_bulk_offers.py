from odoo import fields, models


class EstatePropertyBulkOffers(models.TransientModel):
    _name = "estate.property.bulk.offers"
    _description = "Estate Property Bulk Offers"

    price = fields.Float(required=True)
    validity = fields.Integer(required=True, string="Validity (days)", default=7)
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)

    def action_make_bulk_offers(self):
        estate_properties = self.env["estate.property"].browse(
            self._context.get("active_ids", [])
        )
        for property in estate_properties:
            self.env["estate.property.offer"].create(
                {
                    "price": self.price,
                    "validity": self.validity,
                    "partner_id": self.partner_id.id,
                    "property_id": property.id,
                }
            )
        return {"type": "ir.actions.act_window_close"}

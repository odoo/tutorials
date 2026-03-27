from odoo import models, fields
from odoo.exceptions import UserError


class PropertyOfferWizard(models.TransientModel):
    _name = "property.offer.wizard"
    _description = "Property Offer Wizard"

    property_ids = fields.Many2many("estate.property", readonly=True)
    partner_id = fields.Many2one("res.partner", required=True)
    price = fields.Float(required=True)
    validity = fields.Integer()

    def action_create_offer(self):
        if not self.property_ids:
            raise UserError("Please select at least one property!")

        for property in self.property_ids:
            if property.state in ("new", "offer_received") and (
                property.best_price < self.price
            ):
                self.env["estate.property.offer"].create(
                    {
                        "property_id": property.id,
                        "partner_id": self.partner_id.id,
                        "price": self.price,
                        "validity": self.validity,
                    }
                )

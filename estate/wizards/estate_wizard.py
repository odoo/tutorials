from odoo import models, fields
from odoo.exceptions import UserError


class EstateAddOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "wizard to make a offer for multiple properties"

    price = fields.Float(string="Offer Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    validity = fields.Integer(string="Validity(days)", default=7)

    def add_offer(self):
        property_ids = self.env["estate.property"].browse(
            self._context.get("active_ids", [])
        )
        for property in property_ids:
            if property.state == "sold" or property.state == "offer_accepted":
                raise UserError(f"Property {property.name} is already sold.")
            self.env["estate.property.offer"].create(
                {
                    "property_id": property.id,
                    "validity": self.validity,
                    "price": self.price,
                    "partner_id": self.partner_id.id,
                }
            )

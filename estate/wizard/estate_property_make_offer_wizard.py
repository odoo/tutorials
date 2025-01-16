from odoo import models, fields
from odoo.exceptions import UserError

class EstatePropertyMakeOffer(models.TransientModel):
    _name = "estate.property.make.offer"
    _description = "wizard to make offers in bulk."

    offer_price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity", default=7)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    def make_offer(self):
        for property_id in self.env.context.get('active_ids', []):
            property = self.env['estate.property'].browse(property_id)
            try:
                self.env["estate.property.offer"].create(
                    {
                        "price": self.offer_price,
                        "property_id": property_id,
                        "partner_id": self.partner_id.id,
                        "validity": self.validity,
                    }
                )

            except Exception:
                raise UserError(f"Cannot add any offer to property \"{property.name}\" with id {property_id}")

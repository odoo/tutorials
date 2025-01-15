from odoo import models, fields, exceptions

class EstatePropertyMakeOffer(models.TransientModel):
    _name = "estate.property.make.offer"
    _description = "wizard to make offers in bulk."

    property_ids = fields.Many2many("estate.property", string="Properties", required=True)
    offer_price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity", default=7)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    def make_offer(self):
        for property in self.property_ids:
            try:
                self.env["estate.property.offer"].create(
                    {
                        "price": self.offer_price,
                        "property_id": property.id,
                        "partner_id": self.partner_id.id,
                        "validity": self.validity,
                    }
                )

            except Exception:
                raise exceptions.UserError(f"Cannot add any offer to property \"{property.name}\" with id {property.id}")


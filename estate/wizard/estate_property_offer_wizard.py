from odoo import models, fields


class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Wizard to add an offer to a property"

    price = fields.Float(string="Offer Price")
    validity = fields.Integer(string="Validity")
    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        required=True,
        # default=lambda self: self.env.partner.id,
    )
    # property_ids = fields.Many2many("estate.property", required=True)

    def action_make_offer(self):
        selected_properties = self.env.context.get("active_ids")
        for property_id in selected_properties:
            self.env["estate.property.offer"].create(
                {
                    "property_id": property_id,
                    "price": self.price,
                    "validity": self.validity,
                    "partner_id": self.partner_id.id,
                }
            )
        return True

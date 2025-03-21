from odoo import fields, models


class addOfferWizard(models.TransientModel):
    _name = "add.offer.wizard"
    _description = "Wizard to make an offer on a property"

    price = fields.Float(string="Offer Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    def make_offer(self):
        property_ids = self.env.context.get(
            "active_ids", []
        )  # property ids of selected in list view
        if property_ids:
            offers = []
            for property_id in property_ids:
                offers.append(
                    {
                        "price": self.price,
                        "partner_id": self.partner_id.id,
                        "property_id": property_id,
                    }
                )
            self.env["estate.property.offer"].create(offers)

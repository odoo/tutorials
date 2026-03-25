from odoo import _, fields, models
from odoo.exceptions import UserError


class SendOfferWizard(models.TransientModel):
    _name = "estate.offer.wizard"
    _description = "Estate Offer"

    property_type_id = fields.Many2one("estate.property.type")
    offer_price = fields.Integer("Offer Price")
    customer_id = fields.Many2one("res.partner", string="Buyer", required=True)

    def do_action(self):
        if self.offer_price <= 0:
            raise UserError(_("Offer price must be greater than zero."))
        min_wizard = self.offer_price * 0.9
        properties = self.env["estate.property"].search(
            [
                ("property_type_id", "=", self.property_type_id.id),
                ("expected_price", "<=", self.offer_price),
                ("best_price", "<", min_wizard),
                ("state", "in", ["new", "offer_received"]),
            ],
        )
        offers = []
        for property in properties:
            offers.append(
                {
                    "price": self.offer_price,
                    "validity": 90,
                    "partner_id": self.customer_id.id,
                    "property_id": property.id,
                },
            )
        self.env["estate.property.offer"].create(offers)

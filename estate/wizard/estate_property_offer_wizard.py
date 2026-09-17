from odoo import _, fields, models
from odoo.exceptions import UserError


class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Estate Property Offer Wizard"

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        required=True,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    price = fields.Float(string="Offer Price", required=True)

    def action_create_offers(self):
        properties = self.env["estate.property"].search(
            [
                ("property_type_id", "=", self.property_type_id.id),
                ("state", "in", ("new", "offer_received")),
            ]
        )

        if not properties:
            raise UserError(
                _("No properties found for the selected type that can accept offers.")
            )

        valid_properties = properties.filtered(lambda p: p.best_price < self.price)

        if not valid_properties:
            raise UserError(
                _(
                    "No properties of this type can accept this offer price. Ensure the price is higher than the current best price of the properties."
                )
            )
        offer_vals = []
        for prop in valid_properties:
            offer_vals.append(
                {
                    "property_id": prop.id,
                    "partner_id": self.partner_id.id,
                    "price": self.price,
                }
            )

        if offer_vals:
            self.env["estate.property.offer"].create(offer_vals)

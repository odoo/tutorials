from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):

    _inherit = 'estate.property.offer'

    def accept_offer(self):
        if self.property_id.bid_type == "auction":
            raise ValidationError(
                "You cannot manually accept an offer for an auction property. "
                "The highest bid will be accepted automatically when the auction ends."
            )
        return super().accept_offer()

    @api.model_create_multi
    def create(self, vals_list):
        new_records = self.env["estate.property.offer"].browse([])

        try:
            for vals in vals_list:
                property_id = self.env["estate.property"].browse(vals["property_id"])
                offer_price = float(vals.get("price", 0))
                expected_price = property_id.expected_price or 0

                if property_id.status in ["sold", "offer_accepted"]:
                    raise ValidationError(
                        f"Offers cannot be created! Property '{property_id.name}' is already sold or an offer has been accepted!"
                    )

                if property_id.bid_type == "auction":
                    if offer_price < expected_price:
                        raise ValidationError(
                            f"The offer price for '{property_id.name}' must be higher than the expected price ({expected_price})."
                        )
                else:
                    best_price = property_id.best_price
                    if offer_price < best_price:
                        raise ValidationError(
                            f"The offer price for {property_id.name} must be higher than the existing received offer of {best_price}."
                        )

                property_id.status = "offer_received"

            record = super(models.Model, self).create([vals])
            new_records |= record

            for rec in new_records:
                if rec.property_id:
                    rec.property_id._compute_best_price()

        except Exception as e:
            raise ValidationError(
                f"An error occurred while creating the offer: {str(e)}"
            )

        return new_records

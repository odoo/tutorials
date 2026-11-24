from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False
    )
    buyer_id = fields.Many2one(
        "res.partner",
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
        required=True
    )
    
    def action_accept(self):
        self.ensure_one()

        property_record = self.property_id

        if property_record.state in ("sold", "cancelled"):
            raise UserError(
                self.env._(
                    "A sold or cancelled property cannot accept offers."
                )
            )

        if property_record.offer_ids.filtered(
            lambda offer: offer.status == "accepted" and offer != self
        ):
            raise UserError(
                self.env._("Another offer has already been accepted.")
            )

        # Refuse all other offers
        other_offers = property_record.offer_ids - self
        other_offers.write({"status": "refused"})

        # Accept the selected offer
        self.status = "accepted"

        # Update the property
        property_record.buyer_id = self.buyer_id
        property_record.selling_price = self.price
        property_record.state = "offer_accepted"

    def action_refuse(self):
        self.ensure_one()
        if self.status == 'accepted':
            raise UserError(self.env._('An accepted offer cannot be refused.'))
        self.status = 'refused'
    
    _sql_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer price must be strictly positive.",
    )
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_record = self.env["estate.property"].browse(vals["property_id"])

            if any(offer.price > vals["price"] for offer in property_record.offer_ids):
                raise UserError("You cannot create an offer lower than an existing offer.")

            property_record.state = "offer_received"

        return super().create(vals_list)

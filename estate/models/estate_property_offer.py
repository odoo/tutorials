from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserWarning


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float("Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(days=offer.validity)
            else:  # Fallback if create_date is not set
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            elif offer.date_deadline:  # Fallback if create_date is not set
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept_offer(self):
        for offer in self:
            # Check if there's already an accepted offer
            other_offers = offer.property_id.offer_ids - offer
            if any(other_offers.filtered(lambda o: o.status == "accepted")):
                raise UserWarning("An offer has already been accepted for this property.")
            offer.status = "accepted"
            # Refuse other offers for the same property
            other_offers.write({"status": "refused"})
            # Update the property status
            offer.property_id.status = "offer_accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.partner_id = offer.partner_id
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
        return True

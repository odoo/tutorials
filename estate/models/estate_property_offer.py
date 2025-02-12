from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Propert offers"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        copy="False",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        store=True,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _sql_constraints = [
        ("check_offer_price", "CHECK(price > 0)", "Offer price must be > 0")
    ]

    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            property = record.get('property_id')
            if property:
                existing_offers = self.search([('property_id', '=', property)])
                if any(offer.price >= record.get('price', 0) for offer in existing_offers):
                    raise UserError("An existing offer has an equal or higher amount. Please submit a higher offer.")
    
            self.env['estate.property'].browse(record['property_id']).state = "recevied"
        return super().create(vals)

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(
                    days=offer.validity
                )
            else:
                offer.date_deadline = fields.Date.today() + timedelta(
                    days=offer.validity
                )

    def _inverse_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def accept_offer(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError("This offer has already been accepted.")

            # Accept the current offer
            offer.status = "accepted"
            offer.property_id.state = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.partner_id = offer.partner_id.id

            # Reject all other offers for the same property
            for other_offer in offer.property_id.offer_ids:
                if other_offer.id != offer.id:
                    other_offer.status = "refused"
        return True

    def reject_offer(self):
        for offer in self:
            if offer.status == "refused":
                raise UserError(f"Offer {offer.id} is already refused.")

            if offer.status == "accepted":
                offer.property_id.selling_price = 0
                offer.property_id.partner_id = False

            offer.status = "refused"
        return True



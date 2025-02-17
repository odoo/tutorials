from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offers"
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
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _sql_constraints = [
        ("check_offer_price", "CHECK(price > 0)", "The offer price must be positive")
    ]

    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            property = self.env['estate.property'].browse(record['property_id'])
            if property:
                if property.state == "sold":
                    raise UserError("You cannot create an offer for a sold property.")
                else:
                    existing_offers = self.search([('property_id', '=', property.id)])
                    if any(offer.price >= record.get('price', 0) for offer in existing_offers):
                        raise UserError("An existing offer has an equal or higher amount. Please submit a higher offer.")
        
                    property.state = "received"
        return super().create(vals)

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def accept_offer(self):
        for offer in self:
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

            if offer.status == "accepted":
                offer.property_id.selling_price = 0
                offer.property_id.partner_id = False

            offer.status = "refused"
        return True

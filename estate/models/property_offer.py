from odoo import models, fields, api
from datetime import timedelta

from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    validity = fields.Integer(default=7)

    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        store=True,
        readonly=True
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days

    partner_id = fields.Many2one("res.partner", required=True)

    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False
    )

    def action_accept_offer(self):
        for offer in self:

            # prevent multiple accepted offers
            accepted = self.search([
                ('property_id', '=', offer.property_id.id),
                ('status', '=', 'accepted')
            ])
            if accepted:
                raise UserError("Only one offer can be accepted for a property.")

            offer.status = 'accepted'

            # update property
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'

    def action_refuse_offer(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError("Accepted offer cannot be refused.")
            offer.status = 'refused'

    property_id = fields.Many2one("estate.property", required=True)

    @api.model
    def create(self, vals):

        property_id = vals.get("property_id")
        amount = vals.get("price")

        if property_id and amount:
            property_rec = self.env["estate.property"].browse(property_id)

            existing_offers = property_rec.offer_ids.mapped("price")

            if existing_offers and amount < max(existing_offers):
                raise UserError("Offer must be higher than existing offers.")

            # update property state
            property_rec.state = "offer_received"

        return super().create(vals)


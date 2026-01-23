from odoo import models, fields, api, exceptions


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity", default=7)
    deadline_date = fields.Date(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        copy=False
    )
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    @api.depends("validity")
    def _compute_deadline_date(self):
        for record in self:
            record.deadline_date = fields.Date.add(record.create_date or fields.Date.today(), days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            record.validity = (record.deadline_date - fields.Date.today()).days

    def accept_offer(self):
        for offer in self:
            if offer.property_id.state == "sold":
                raise exceptions.UserError(f"Property {offer.property_id.name} is already sold")
            elif offer.property_id.state == "offer_accepted":
                raise exceptions.UserError(f"Property {offer.property_id.name} is already accepted")
            elif offer.property_id.state == "cancelled":
                raise exceptions.UserError(f"Property {offer.property_id.name} is cancelled")
            else:
                offer.property_id.buyer = offer.partner_id
                offer.property_id.selling_price = offer.price
                offer.property_id.state = "offer_accepted"
                offer.status = "accepted"
        return True

    def refuse_offer(self):
        for offer in self:
            if offer.property_id.state == "sold":
                raise exceptions.UserError(f"Property {offer.property_id.name} is already sold")
            offer.property_id.buyer = None
            offer.property_id.selling_price = 0
            offer.property_id.state = "offer_received"
            offer.status = "refused"
        return True

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.depends("validity", "property_id")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                fields.Date.today(), days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = (
                    record.create_date.date()
                    if record.create_date
                    else fields.Date.today()
                )
                record.validity = (record.date_deadline - create_date).days

    def accept_offer(self):
        print(self.price)
        for record in self:
            if record.status == "accepted":
                raise UserError("This offer already accepted")

            other_offers = self.search(
                [
                    ("property_id", "=", record.property_id.id),
                    ("id", "!=", record.id),
                ]
            )

            other_offers.write({"status": "refused"})

            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.status = "offer_accepted"

    def refuse_offer(self):
        for record in self:
            if record.status == "refused":
                raise UserError("This offer already refused")
            if record.status == "accepted":
                record.property_id.selling_price = 0
                record.property_id.buyer_id = False
                record.property_id.status = "offer_received"
            record.status = "refused"

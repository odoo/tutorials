from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Integer()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, readonly=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                fields.Date.today(),
                days=record.validity,
            )

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def refuse_offer(self):
        for record in self:
            record.status = "refused"

    def accept_offer(self):
        for record in self:
            accepted_offer = record.property_id.offer_ids.filtered(
                lambda offer: offer.status == "accepted"
            )

            if accepted_offer:
                raise exceptions.UserError(
                    "This property already has an accepted offer."
                )

            record.status = "accepted"

from odoo import models, fields, api
from odoo.exceptions import UserError


class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(
                fields.Date.to_date(create_date), days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.validity = (
                record.date_deadline - fields.Date.to_date(create_date)
            ).days

    def action_accepted_offer(self):
        exists_accepted_offer = self.env["estate.property.offer"].search(
            [
                ("property_id", "=", self.property_id.id),
                ("status", "=", "accepted"),
                ("id", "!=", self.id),
            ]
        )
        if exists_accepted_offer:
            raise UserError("Only one offer can be accepted for a given property")

        property = self.property_id
        property.buyer_id = self.partner_id
        property.selling_price = self.price
        self.status = "accepted"

        other_offers = self.env["estate.property.offer"].search(
            [("property_id", "=", property.id), ("id", "!=", self.id)]
        )
        other_offers.status = "refused"

    def action_refused_offer(self):
        if self.status == "accepted":
            property = self.property_id
            property.buyer_id = False
            property.selling_price = 0.0

        self.status = "refused"

from odoo.exceptions import UserError

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for property"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Date.add(
                    offer.create_date,
                    days=offer.validity,
                )
            else:
                offer.date_deadline = fields.Date.add(
                    fields.Date.today(), days=offer.validity
                )

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise UserError(
                    "a buyer is already assigned , therefore another offer has been accepted"
                )
            offer.status = "accepted"
            offer.property_id.selling_price = self.price
            offer.property_id.buyer_id = self.partner_id

        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
        return True

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date() if offer.create_date else fields.Date.context_today(offer)
            )
            offer.date_deadline = fields.Date.add(start_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date() if offer.create_date else fields.Date.context_today(offer)
            )
            offer.validity = (offer.date_deadline - start_date).days

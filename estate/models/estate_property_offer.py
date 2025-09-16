from odoo import fields, models, api
from datetime import timedelta


class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Offer"

    price = fields.Float(string="Offer Price")
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline"
    )

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for offer in self:
            print("B")
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

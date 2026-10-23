from datetime import timedelta

from odoo.exceptions import ValidationError

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offers"

    price = fields.Float("Price", required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
        readonly=True,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(create_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - create_date) / timedelta(days=1)

    def action_offer_accepted(self):
        self.ensure_one()
        if any(offer.status == "accepted" for offer in self.property_id.offer_ids):
            raise ValidationError("Property has already an ongoing accepted offer")
        self.status = "accepted"
        self.property_id.state = "accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price

    def action_offer_refused(self):
        self.ensure_one()
        self.status = "refused"

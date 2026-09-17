from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="compute_date_deadline", inverse="inverse_date_deadline"
    )

    _check_price = models.Constraint("CHECK(price > 0)", "Price must be positive")

    @api.depends("validity", "create_date")
    def compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = False

    def inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days

    def action_accept(self):
        self.ensure_one()
        accepted_offer = self.env["estate.property.offer"].search(
            [
                ("property_id", "=", self.property_id.id),
                ("status", "=", "accepted"),
                ("id", "!=", self.id),
            ],
            limit=1,
        )

        if accepted_offer:
            return {
                "type": "ir.actions.act_window",
                "name": "Accept Offer",
                "res_model": "estate.property.offer.wizard",
                "view_mode": "form",
                "target": "new",
                "context": {"default_offer_id": self.id},
            }

        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.selling_price = 0.0
            record.property_id.buyer_id = None

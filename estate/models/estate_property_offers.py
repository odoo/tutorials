from odoo import api, fields, models


class PropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer model"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    _check_price = models.Constraint(
        "CHECK(price >= 0)",
        "The price of the offer must be positive."
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add((record.create_date or fields.Datetime.now()), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days if record.date_deadline else record.validity

    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"

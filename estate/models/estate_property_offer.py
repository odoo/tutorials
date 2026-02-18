from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer"
    _order = "sequence, id"

    currency_id = fields.Many2one('res.currency', 'Currency')
    price = fields.Monetary("Price", required=True)

    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], copy=False)

    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", index=True, required=True)

    def _current_date(self):
        return fields.Date.today()

    def _seven_days_from_now_date(self):
        return fields.Date.add(fields.Date.today(), days=7)

    deadline = fields.Date("Deadline", default=_seven_days_from_now_date)
    creation_date = fields.Date("Creation Date", default=_current_date)
    validity = fields.Integer("Validity (days)", store=True, compute="_compute_validity", inverse="_inverse_validity")

    @api.depends("deadline")
    def _compute_validity(self):
        for offer in self:
            offer.validity = (offer.deadline - offer.creation_date).days

    @api.onchange("validity")
    def _inverse_validity(self):
        for offer in self:
            offer.deadline = fields.Date.add(offer.creation_date, days=offer.validity)

    sequence = fields.Integer("Sequence", default=0)

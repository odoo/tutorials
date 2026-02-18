from odoo import fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer"
    _order = "sequence, id"

    currency_id = fields.Many2one('res.currency', 'Currency', readonly=True)
    price = fields.Monetary("Price", required=True)

    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], copy=False)

    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", index=True, required=True)

    def _seven_days_from_now_date(self):
        return fields.Date.add(fields.Date.today(), days=7)

    deadline = fields.Date("Deadline", default=lambda self: self._seven_days_from_now_date())

    sequence = fields.Integer("Sequence", default=0)

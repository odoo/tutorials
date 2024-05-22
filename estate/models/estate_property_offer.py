from odoo import models, fields, api
from odoo.tools import add


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    # Model Fields
    price = fields.Float()
    status = fields.Selection(copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])

    # Relational Fields
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    # Computed Fields
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    # Computation methods
    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.to_date(add(record.create_date, days=record.validity))

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = int((record.date_deadline - fields.Date.to_date(record.create_date)).days)

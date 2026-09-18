from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer description test"

    validity = fields.Integer()
    date_deadline = fields.Date(compute="_compute_validity_date", inverse="_inverse_validity_date")

    @api.depends("create_date", "validity")
    def _compute_validity_date(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_validity_date(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

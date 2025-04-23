from odoo import fields, models
from odoo import api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer for an estate"

    price = fields.Float(string="Price")
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    create_date = fields.Date(default=lambda self: self._get_current_day())
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_validity_date", inverse="_inverse_validity_date")

    @api.depends("create_date", "validity")
    def _compute_validity_date(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_validity_date(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def _get_current_day(self):
        return fields.Date.today()

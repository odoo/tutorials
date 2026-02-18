from datetime import date, timedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date or date.today()
            record.date_deadline = start_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else date.today()
            date_dif = record.date_deadline - start_date
            record.validity = date_dif.days

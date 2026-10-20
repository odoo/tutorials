from odoo import api, fields, models


class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    validity = fields.Integer(default=7, compute="_inverse_date_deadline", inverse="_compute_date_deadline")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    @api.depends("date_deadline", "validity")
    def _inverse_date_deadline(self):
        for record in self:
            if (fields.Date.today() < record.date_deadline):
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 0

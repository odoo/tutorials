from odoo import api, models, fields
from dateutil.relativedelta import relativedelta


class estate_offer(models.Model):
    _name = "estate.property.offer"
    _description = "This is Real Estate property offer"

    price = fields.Float("Price")
    status = fields.Selection(
        string="status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            current_date = fields.Date.today()
            record.date_deadline = current_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            current_date = fields.Date.today()
            if record.date_deadline:
                record.validity = relativedelta(record.date_deadline, current_date).days
            else:
                record.validity = 0

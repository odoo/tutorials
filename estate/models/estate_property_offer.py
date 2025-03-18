from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "My Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([('accept', 'Accept'), ('refused', 'Refused')], copy = False)
    partner_id = fields.Many2one('res.partner', string = "Partner", required = True)
    property_id = fields.Many2one('estate.property', string = 'Property', required = True)

    validity = fields.Integer(string = "Validity", default = 7)
    date_deadline = fields.Date(compute = "_compute_deadline", inverse = "_inverse_deadline", string = "Deadline")

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if not record.create_date:
                record.date_deadline = fields.Date.today() + relativedelta(days = record.validity)
            else:
                record.date_deadline = record.create_date.date() + relativedelta(days = record.validity)

    def _inverse_deadline(self):
        for record in self:
            timedelta = record.date_deadline - record.create_date.date()
            record.validity = timedelta.days

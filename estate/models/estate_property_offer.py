from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Offer"

    price = fields.Float(string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_method", inverse="_inverse_deadline_method")

    @api.depends("create_date", "validity")
    def _compute_deadline_method(self):
        for rec in self:
            create_date = rec.create_date.date() if rec.create_date else fields.Date.today()
            rec.date_deadline = create_date + relativedelta(days=rec.validity)

    def _inverse_deadline_method(self):
        for rec in self:
            create_date = rec.create_date.date() if rec.create_date else fields.Date.today()
            rec.validity = relativedelta(rec.date_deadline, create_date).days

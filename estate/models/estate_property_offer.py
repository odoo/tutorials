from odoo import api, models, fields
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer description"

    price = fields.Float('price')
    status = fields.Selection(
        string='status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = fields.Date.today()
            if record.create_date:
                start_date = record.create_date
            record.date_deadline = start_date + \
                relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = fields.Date.today()
            if record.create_date:
                start_date = record.create_date
            record.validity = (record.date_deadline - fields.Date.today()).days

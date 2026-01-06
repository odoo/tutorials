from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is the table of offer that is received for property"

    price = fields.Float('price')
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create = record.create_date or fields.Date.today()
            record.date_deadline = (create + relativedelta(days=record.validity))

    def _inverse_date_deadline(self):
        for record in self:
            create = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - fields.Date.today(create)).days

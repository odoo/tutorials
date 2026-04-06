from datetime import timedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property offer'

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],
        copy=False)

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(string="Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline",store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            starting_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = starting_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            starting_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - starting_date).days

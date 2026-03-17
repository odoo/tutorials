from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer placed on some property'

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_compute_validity')

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date is not None:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _compute_validity(self):
        for record in self:
            if record.create_date is not None:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days
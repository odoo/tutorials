from odoo import api, fields, models


class Offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer for a property of Estate'

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        index=True,
        required=True,
    )
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                fields.Date.today(),
                days=record.validity,
            )

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days

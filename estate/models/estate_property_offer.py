from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'All offers'

    price = fields.Float(required=True)
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
    )
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse="_inverse_deadline")

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            created_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(
                created_date, days=record.validity,
            )

    def _inverse_deadline(self):
        for record in self:
            created_date = record.create_date.date() or fields.Date.today()
            record.validity = (record.date_deadline - created_date).days

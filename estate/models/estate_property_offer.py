from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused'), ('ongoing', 'Ongoing')], required=True, copy=False, default='ongoing')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(
        'Validity (in days)',
        default=5,
    )
    date_deadline = fields.Date(
        'Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    @api.depends("date_deadline", "create_date")
    def _inverse_date_deadline(self):
        for record in self:
            created_d = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - created_d).days

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            created_d = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(created_d, days=record.validity)

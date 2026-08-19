from odoo import models, fields, api

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    validity = fields.Integer(default=7)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if not record.date_deadline:
                continue
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - base_date).days

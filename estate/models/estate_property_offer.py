from odoo import api, fields, models
from datetime import date, timedelta


class EsatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string="Deadline", store=True)

    @api.depends('validity','property_id.create_date')
    def _compute_deadline(self):
        for record in self:
            if record.validity and record.property_id.create_date:
                record.date_deadline = record.property_id.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False
    
    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline and record.property_id.create_date:
                record.validity = (record.date_deadline - record.property_id.create_date.date()).days
            else:
                record.validity = 0

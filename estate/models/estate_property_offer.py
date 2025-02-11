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

    def offer_accepted_action(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
            for offer in record.property_id.offer_ids:
                if offer.id is not record.id:
                    offer.status = 'refused'

    def offer_refused_action(self):
        for record in self:
            record.status = 'refused'
            if(record.property_id.partner_id == record.partner_id):
                record.property_id.selling_price = 0
                record.property_id.partner_id = False   

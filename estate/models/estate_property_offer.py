from datetime import date, timedelta

from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused'),
        ],
    )
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string="Deadline")
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name='estate.property',
        required=True,
    )
    
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
    
    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
        return True
    
    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True

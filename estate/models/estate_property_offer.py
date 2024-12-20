from odoo import fields, api, models
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'real estate property offer'

    price= fields.Float()
    status= fields.Selection(
        selection=[
        ('accepted','Accepted'),
        ('refused','Refused'),],
        copy=False
    )
    partner_id=fields.Many2one('res.partner', required=True)
    property_id=fields.Many2one('estate.property', required=True)
    validity=fields.Integer(default=7)
    date_deadline=fields.Date('date_deadline',compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 0


    
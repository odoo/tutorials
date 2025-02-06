from odoo import models,fields, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="estate property offer table"

    price = fields.Float("Price")
    status = fields.Selection(
        string='Status',
        selection=[('accepted', "Accepted"), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    create_date = fields.Date()
    
    validity =fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_inverse_deadline')

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)

            else:
                offer.date_deadline = False
    
    def _inverse_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                dayys = (offer.date_deadline - offer.create_date).days
                offer.validity = dayys


# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details. 

from odoo import api, models, fields
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float('Offer Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
   
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string="Validity",default=7)
    date_deadline = fields.Date(compute = "_compute_date_deadline" , inverse = "_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline=(record.create_date  or fields.Date.today()) + relativedelta(days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity=(record.date_deadline - fields.Date.today()).days or 0

    def action_accept(self):
        if self.status == 'accepted':
            raise UserError("Offer has already been accepted!")
        self.write({'status':'accepted'})
        for property in self.mapped('property_id'):
            property.write({
                'state': 'offer_accepted',
                'selling_price': self.price,
                'buyer_id': self.partner_id,
            })
    def action_refuse(self):
        if self.status == 'refused':
            raise UserError("Offer has already been refused!")
        self.write({'status':'refused'})

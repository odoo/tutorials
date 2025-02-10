from odoo import models,fields,api

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _discription = 'Estate Property Offers'
    _order = 'price desc'

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="status",
        selection=[
            ('accepted','Accepted'),
            ('rejected','Rejected')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id',string='Property Type')

    def action_status_accept(self):
        for record in self:
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'

    def action_status_reject(self):
        for record in self:
            record.status = 'rejected'
            record.property_id.state = 'offer_rejected'

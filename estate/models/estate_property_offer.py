from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    
    price = fields.Float(required=True)
    property_id = fields.Many2one('estate.property')
    buyer_id = fields.Many2one('res.partner')
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline")
    offer_status = fields.Selection([
        ('offer_received', 'New Offer'),
        ('offer_accepted', 'Offer Accepted'),
        ('offer_rejected', 'Offer Rejected')
    ], default='offer_received', required=True)

    
    def action_accept_offer(self):
        self.offer_status = 'offer_accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.buyer_id
    def action_reject_offer(self):
        self.offer_status = 'offer_rejected'

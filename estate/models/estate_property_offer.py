from odoo import api,models, fields

from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float('Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status',copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer("Validity (days)", default="7")
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("property_id.date_availability", "validity")
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = offer.property_id.date_availability + timedelta(days=offer.validity)


    def _inverse_deadline(self):
        for offer in self:
            deadline_date = fields.Date.from_string(offer.date_deadline)
            availability_date = fields.Date.from_string(offer.property_id.date_availability)    
            offer.validity = (deadline_date - availability_date).days

    def offer_confirm(self):
        for offer in self:
            offer.status="accepted"
            offer.property_id.partner_id=offer.partner_id
            offer.property_id.selling_price=offer.price
    
    def offer_cancel(self):
        for offer in self:
            offer.status="refused"
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price>=0 )',
         'The price must be strictly positive.')
    ]

            


    


        
    
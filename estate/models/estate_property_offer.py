from dateutil.relativedelta import relativedelta
from odoo import exceptions, models, fields, tools, api

class PropertyOffer(models.Model):    
    # Model properties
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    
    # Model fields
    price = fields.Float()
    
    status = fields.Selection(selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False)
    # Button Object
    def offer_object_button_accepted(self):
        for offer in self:
            if offer.property_id.state == 'offerreceived' or offer.property_id.state == 'new':
                offer.property_id.selling_price = offer.price
                offer.property_id.state = 'offeraccepted'
                offer.property_id.buyer_id = offer.partner_id
                offer.status = 'accepted'
            else:
                raise exceptions.UserError("Cannot accept more than one offer per property")
    
    def offer_object_button_refused(self):
        for offer in self:
            offer.status = 'refused'
    
    
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    
    
    # Calculate
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse="_inverse_date_deadline")
    
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity) 

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days
            
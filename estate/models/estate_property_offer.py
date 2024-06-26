from attr import field
from odoo import models, fields, tools, api

class PropertyOffer(models.Model):    
    # Model properties
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    
    # Model fields
    price = fields.Float()
    status = fields.Selection(selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    
    # Calculate
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_calc_date_deadline', inverse="_calc_inverse_date_deadline")
    @api.depends("validity")
    def _calc_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.add(offer.create_date, days=offer.validity)
    
    # @api.depends("date_deadline")
    # def _calc_inverse_date_deadline(self):
        # for offer in self:
            # offer.validity = 
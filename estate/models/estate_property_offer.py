# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = 'price desc'
    
    price = fields.Float(string="Price")
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    property_id = fields.Many2one(comodel_name='estate.property', string="Property", required=True)
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string="Property Type", related='property_id.property_type_id', store=True)
    validity = fields.Integer(string="Validity")
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline', default=lambda self:fields.Date.today())
    status = fields.Selection(
                  selection=[
                        ('accepted', "Accepted"),
                        ('refused', "Refused")
                        ],
                  string="status", copy=False)
    _sql_constraints = [
            ('check_price', "CHECK(price >= 0)", "Price should be positive")
    ]
    
    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline=(offer.create_date  or fields.Date.today()) + relativedelta(days = offer.validity)
    
    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity=(offer.date_deadline - fields.Date.today()).days or 0       
    
    def action_accepted(self):
            if (self.property_id.state != 'offer_accepted' and self.status != 'accepted'):
                    self.status='accepted'
                    self.property_id.selling_price = self.price
                    self.property_id.partner_id = self.partner_id
                    self.property_id.state='offer_accepted'
            else:
                    raise UserError(_("Only one offer can be accepted for a property. Please reject the current offer before accepting a new one."))

    def action_refused(self):
            self.status='refused'   
       
    @api.constrains('price')        
    def _check_price(self):
            for offer in self:
                    if(offer.price < (offer.property_id.expected_price * 90) / 100):
                           raise UserError(_("The offer price must be at least 90% of the property's expected price. Please increase your offer."))

    @api.model_create_multi
    def create(self, offer_list):
            for offer in offer_list:
                    if offer['property_id']:
                            property = self.env['estate.property'].browse(offer['property_id'])
                    if property.state == 'sold':
                            raise UserError(_("This property has already been sold and cannot accept new offers."))
                    if offer['price'] < property.best_price:
                            raise UserError(_("Your offer price must be higher than the current best offer price of %.2f."))  
                    if property.state == 'new':
                            property.state = 'offer_received'      
            return super().create(offer_list)       

from odoo import models, fields, api, exceptions
from datetime import date
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for estate properties."
    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK (price > 0)', 'Offer price must be positive.'),
    ]
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Buyer', index=True, required=True)
    property_id = fields.Many2one('estate.property', string='Property', index=True, required=True, ondelete='cascade')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date()

    @api.model_create_multi
    def create(self, vals_list):
        # Check price validation before creating offers
        for vals in vals_list:
            if 'property_id' in vals and 'price' in vals:
                property_obj = self.env['estate.property'].browse(vals['property_id'])
                if property_obj.best_price > 0 and vals['price'] <= property_obj.best_price:
                    raise exceptions.ValidationError(
                        f"Offer price ({vals['price']}) must be greater than the property's best price ({property_obj.best_price})."
                    )
        
        offers = super().create(vals_list)
        # Update property state to 'offer_received' when an offer is created
        for offer in offers:
            if offer.property_id and offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'
        return offers

    @api.onchange('validity')
    def _onchange_validity(self):
        if self.validity:
            base_date = self.create_date.date() if self.create_date else date.today()
            self.date_deadline = base_date + relativedelta(days=self.validity)

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        if self.date_deadline:
            base_date = self.create_date.date() if self.create_date else date.today()
            delta = self.date_deadline - base_date
            self.validity = delta.days

    def action_confirm_offer(self):
        for record in self:
            # Refuse all other offers for this property
            other_offers = record.property_id.offer_ids.filtered(lambda x: x.id != record.id)
            other_offers.write({'status': 'refused'})
            
            # Accept this offer
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.status = 'accepted'


    def action_cancel_offer(self):
        for record in self:
            record.status = 'refused'

    

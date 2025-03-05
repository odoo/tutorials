from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    selling_mode = fields.Selection(related='property_id.selling_mode', store=True, readonly=True)
    
    def action_accept(self):
        """Override to send email notifications"""
        result = super(EstatePropertyOffer, self).action_accept()
        
        # Send acceptance email to the accepted offer's partner
        if self.env.context.get('no_mail'):
            return result
            
        template_accepted = self.env.ref('estate_auction.email_template_offer_accepted')
        if template_accepted:
            template_accepted.send_mail(self.id, force_send=True)
        
        # Send rejection emails to all other offers for this property
        template_rejected = self.env.ref('estate_auction.email_template_offer_rejected')
        if template_rejected:
            other_offers = self.property_id.offer_ids.filtered(lambda o: o.id != self.id)
            for offer in other_offers:
                template_rejected.send_mail(offer.id, force_send=True)
        
        return result

from odoo import models, fields

class EcommerceProductOffer(models.Model):
    _name = 'ecommerce.product.offer'
    _description = 'Ecommerce Product Offer'

    name = fields.Char(string='Offer Name', required=True)
    product_id = fields.Many2one('ecommerce.product', string='Product', required=True)
    discount_percentage = fields.Float(string='Discount Percentage', required=True, help="Discount percentage for the offer")
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    status = fields.Boolean(string='Active', default=True, help="Indicates if the offer is currently active")


    def action_accept_offer(self):
        if 'accepted' in self.mapped('product_id.offer_ids.status'):
            raise ValueError("There is already an accepted offer for this product.")
        self.write({'status': 'accepted'})
        return self.mapped('product_id').write({
            'state': 'offer_accepted',
            'selling_price': self.product_id.price * (1 - self.discount_percentage / 100),
        })
            
    def action_reject_offer(self):
        self.write({'status': 'rejected'})
        return self.mapped('product_id').write({
            'state': 'offer_rejected',
        })

    
                
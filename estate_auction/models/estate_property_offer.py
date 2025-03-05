from odoo import api,fields, models 
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):

    _inherit='estate.property.offer'
    
    def action_accept(self):
        if self.property_id.auction_type == 'auction':
            raise UserError("Offers cannot be manually accepted for auction properties.")
        super(EstatePropertyOffer, self).action_accept()

  
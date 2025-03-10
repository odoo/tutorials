from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    sell_type = fields.Selection(related="property_id.sell_type")

    @api.model_create_multi
    def create(self, vals_list):
        if not vals_list:
            return super().create(vals_list)
        property_id = vals_list[0].get('property_id')
        if not property_id:
            raise ValidationError("Property reference is missing.")
        if property.auction_end_time < fields.datetime.now():
            raise ValidationError("Offer can't created after auction end.")    
        property = self.env['estate.property'].browse(property_id)
        for vals in vals_list:
            if property.state == 'sold':
              raise UserError("You cannot create an offer for a sold property.")
        for vals in vals_list:
            if vals['property_id']:
                if property.expected_price > vals['price']:
                    raise ValidationError(
                        "You cannot create an offer lower than expected price."
                    )
        if property.sell_type == 'auction':
            return models.Model.create(self, vals_list)            
        return super().create(vals_list)
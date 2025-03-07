from odoo import api, models
from odoo.exceptions import UserError,ValidationError

class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_obj = self.env['estate.property'].browse(val['property_id'])
            if property_obj.selling_method != 'auction':
                return super(EstatePropertyOffer, self).create(vals)

            if property_obj.state == 'sold':
                raise ValidationError("You cannot make an offer on a sold property.")

            if property_obj.state == 'new' or not property_obj.state:
                self.env['estate.property'].browse(val['property_id']).state = 'offer_received'

            min_price = self.env['estate.property'].browse(val['property_id']).expected_price
            if val['price'] <= min_price:
                raise ValidationError("The price must be higher than the expected price.")

            return models.Model.create(self, vals)

   
    def action_accept_offer(self):
        if self.property_id.selling_method == 'auction':
            raise UserError("An offer cannot be confirmed for a property listed in an auction.")
        super(EstatePropertyOffer, self).action_accept_offer()

    def action_refuse_offer(self):
        if self.property_id.selling_method == 'auction':
            raise UserError("An offer cannot be refused for a property listed in an auction.")

        super(EstatePropertyOffer, self).action_refuse_offer()

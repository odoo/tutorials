from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatepropertyOffer(models.Model):
    _inherit= 'estate.property.offer'

    is_auction = fields.Boolean(compute="_compute_is_auction")

    @api.depends('property_id.selling_type')
    def _compute_is_auction(self):
        for record in self:
            record.is_auction = record.property_id.selling_type == 'auction'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            new_offer_price = vals.get('price')
            if property_id:
                property = self.env['estate.property'].browse(property_id) 
                property.state = 'offer_received'
                if property.selling_type == 'regular':
                    return super().create(vals_list)
                else:
                    if property.expected_price > float(new_offer_price):
                        raise UserError(f"Offre must be higher then expected price {property.expected_price}")
        return models.Model.create(self,vals_list)
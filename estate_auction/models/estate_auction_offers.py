from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateAuctionOffer(models.Model):
    _inherit = 'estate.property.offer'

    is_button_hidden = fields.Boolean(compute='_compute_button_visibility', store=False)

    @api.depends('property_id.sale_mode')
    def _compute_button_visibility(self):
        for offer in self:
            offer.is_button_hidden = (
                offer.property_id.sale_mode == 'auction'
            )

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            prop = self.env['estate.property'].browse(val.get('property_id'))
            price = val.get('price', 0)

            if prop.sale_mode == 'auction':
                if price < prop.expected_price:
                    raise UserError(
                        "Auction offer cannot be lower than the expected price."
                    )
            else:
                return super().create(vals_list)

            prop.write({'state': 'offer_received'})
        return models.Model.create(self, vals_list)

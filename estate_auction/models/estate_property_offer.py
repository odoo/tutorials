from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    property_sale_format = fields.Selection(related='property_id.property_sale_format', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals['property_id']:
                property = self.env['estate.property'].browse(vals['property_id'])
                if property.expected_price > vals['price']:
                    raise ValidationError(
                        "You cannot create an offer lower than expected price."
                    )
        return models.Model.create(self, vals_list)

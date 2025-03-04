from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    property_sale_format = fields.Selection(related='property_id.property_sale_format', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        if not vals_list:
            return super().create(vals_list)
        property_id = vals_list[0].get('property_id')
        if not property_id:
            raise ValidationError("Property reference is missing.")
        # Fetch the property once
        property = self.env['estate.property'].browse(property_id)
        for vals in vals_list:
            if vals['property_id']:
                if property.expected_price > vals['price']:
                    raise ValidationError(
                        "You cannot create an offer lower than expected price."
                    )
        if property.property_sale_format == 'auction':
            return models.Model.create(self, vals_list)
        return super().create(vals_list)

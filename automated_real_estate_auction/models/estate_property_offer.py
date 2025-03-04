from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    sell_type = fields.Selection(related='property_id.sell_type', store=True)

    @api.model_create_multi
    def create(self, vals):
        if isinstance(vals, list) and vals:
          vals = vals[0]
        property_id = vals.get('property_id')
        if not property_id:
            raise ValueError("Missing 'property_id' in values")

        property = self.env['estate.property'].browse(property_id)
        if vals['price'] < property.expected_price:
            raise exceptions.UserError(f"offer price must not be lower than expected price :  {property.expected_price}")
        return super(EstatePropertyOffer, self).create(vals)

    def action_accept(self):
        if self.sell_type == 'auction' and self.property_id.stage in ['template', 'sold']:
          raise exceptions.UserError("Property can not be sold during auction process")

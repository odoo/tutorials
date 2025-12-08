from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_multilocation = fields.Boolean(compute="_compute_is_multilocation")

    @api.depends('product_variant_ids.stock_quant_ids.location_id')
    def _compute_is_multilocation(self):
        for record in self:
            internal_location_ids = {
                loc.id
                for loc in record.mapped(
                    'product_variant_ids.stock_quant_ids.location_id'
                )
                if loc.usage == 'internal'
            }
            record.is_multilocation = len(internal_location_ids) > 1

from odoo import api, models


class InheritedProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _load_pos_data_fields(self, config):
        params = super()._load_pos_data_fields(config)
        params.append('pos_second_uom_id')
        return params

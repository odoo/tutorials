from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _load_pos_data_fields(self, config_id):
        params = super()._load_pos_data_fields(config_id)
        params.append('self_order_description')
        return params

from odoo import api,models,fields


class ProductProduct(models.Model):
    _inherit = ['product.product']

    @api.model
    def _load_pos_data_fields(self, config_id):
        params = super()._load_pos_data_fields(config_id) 
        params += ['is_kit','sub_product_ids']
        return params

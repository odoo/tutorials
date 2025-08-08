from odoo import api, models


class Product(models.Model):
    _inherit = 'product.product'

    @api.model
    def _load_pos_data_fields(self, config_id):
        pos_fields = super()._load_pos_data_fields(config_id)
        pos_fields.extend(['pos_second_uom_id'])
        return pos_fields

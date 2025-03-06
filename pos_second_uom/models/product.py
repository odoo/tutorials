from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields.append("sec_uom_id")
        return fields

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_product_info_pos(self, price, quantity, pos_config_id):
        product_info = super().get_product_info_pos(
            price,
            quantity,
            pos_config_id)

        product_info.update(
            weight=self.weight,
            weight_uom_name=self.weight_uom_name,
            volume=self.volume,
            volume_uom_name=self.volume_uom_name
        )
        return product_info

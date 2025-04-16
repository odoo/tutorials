from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_action_add_from_catalog_extra_context(self):
        return {
            **super()._get_action_add_from_catalog_extra_context(),
            'display_uom': self.env.user.has_group('uom.group_uom'),
        }

    def _get_product_catalog_order_data(self, products, **kwargs):
        res = super()._get_product_catalog_order_data(products, **kwargs)
        for product in products:
            res[product.id]['uom'] = {
                'display_name': product.uom_id.display_name,
                'id': product.uom_id.id,
            }
        return res

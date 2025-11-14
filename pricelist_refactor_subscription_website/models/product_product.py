from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_pricelist_item_ids(self, pricelist, date, product=None):
        return self.product_tmpl_id._get_pricelist_item_ids(pricelist, date, product=self)

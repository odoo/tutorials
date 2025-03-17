from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_product_catalog_lines_data(self, **kwargs):
        res = super()._get_product_catalog_lines_data(**kwargs)
        if len(self) == 1:
            res.update({
                'uom': {
                    'display_name': self.product_id.uom_id.display_name,
                    'id': self.product_id.uom_id.id,
                },
            })
            if self.product_id.uom_id != self.product_uom:
                res['sale_uom'] = {
                    'display_name': self.product_uom.display_name,
                    'id': self.product_uom.id,
                }
            return res
        else:
            return res

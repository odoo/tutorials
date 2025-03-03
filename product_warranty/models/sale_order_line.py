from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'linked_line_id', 'linked_line_ids')
    def _compute_name(self):
        # when adding product warranty line skip this method for computing name.
        product_warranty = self.env.ref('product_warranty.extended_warranty_product', raise_if_not_found=False)
        super(SaleOrderLine, self.filtered(lambda l: not l.product_id == product_warranty))._compute_name()

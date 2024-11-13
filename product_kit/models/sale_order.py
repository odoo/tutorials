from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_print_sub_products = fields.Boolean(string="Print in report?")

    @api.onchange('order_line')
    def _remove_sub_products(self):
        for record in self:
            main_product_ids = set()
            for so_line in record.order_line:
                main_product_ids.add(so_line._origin.id) if not so_line.parent_id else ()
            for so_line in record.order_line:
                if so_line.parent_id and so_line.parent_id.id not in main_product_ids:
                    record.order_line -= so_line

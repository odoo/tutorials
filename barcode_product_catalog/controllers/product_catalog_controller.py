from odoo import http
from odoo.http import request


class ProductCatalogController(http.Controller):

    @http.route('/product/catalog/sorted_product_ids', type='json', auth='user')
    def get_sorted_product_ids(self, order_id, res_model):
        if res_model not in ['sale.order', 'purchase.order']:
            return []

        if res_model == 'sale.order':
            line_model = 'sale.order.line'
            qty_field = 'product_uom_qty'
        else:
            line_model = 'purchase.order.line'
            qty_field = 'product_qty'

        all_records = request.env['product.product'].search([]).ids

        line_data = request.env[line_model].read_group(
            domain=[('order_id', '=', order_id)],
            fields=[qty_field],
            groupby=['product_id'],
            orderby=f'{qty_field} desc'
        )

        product_qty_map = {
            entry['product_id'][0]: entry[qty_field]
            for entry in line_data if entry['product_id']
        }

        ordered_products = sorted(
            product_qty_map.items(),
            key=lambda x: x[1],
            reverse=True
        )
        ordered_products = [pid for pid, qty in ordered_products]

        unordered_products = list(set(all_records) - set(ordered_products))

        full_sorted_ids = ordered_products + unordered_products
        return full_sorted_ids

from datetime import datetime
from odoo import api, models
from odoo.osv import expression


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        '''Modify product dropdown in sale order line to show last sold date'''

        domain = args or []
        partner_id = self.env.context.get('partner_id')
        order_type = self.env.context.get('order_type')
        active_id = self.env.context.get('active_id')
        if not order_type and active_id:
            order_type = self.env['account.journal'].browse(active_id).type

        if partner_id:
            last_ordered_products = {}
            if order_type == 'sale':
                last_ordered_products = self._get_last_sold_products(partner_id)

                product_ids = list(last_ordered_products.keys())

                products = self.search_fetch(expression.AND([domain, [('id', 'in', product_ids)], [("name", operator, name)]]), ['display_name'], limit=limit)
                limit_rest = limit and limit - len(products)
                if limit_rest is None or limit_rest > 0:
                    products |= self.search_fetch(expression.AND([domain, [('id', 'not in', product_ids)], [("name", operator, name)]]), ['display_name'], limit=limit_rest)
                products = sorted(products, key=lambda p: last_ordered_products.get(p.id, datetime.min), reverse=True)

                return [(product.id, product.display_name, self.env['product.template']._get_time_ago_string(last_ordered_products.get(product.id, False))) for product in products]

        return super().name_search(name, args, operator, limit)

from datetime import datetime
from odoo import api, fields, models
from odoo.osv import expression


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    last_order_time = fields.Datetime(compute='_compute_last_order_time')
    last_date_str = fields.Char(compute='_compute_last_order_time')

    @api.depends_context('order_id')
    def _compute_last_order_time(self):
        """Compute the last order time for each product based on the latest sale or purchase."""

        partner_id = self.env.context.get('partner_id')
        order_type = self.env.context.get('order_type')

        if not partner_id:
            for record in self:
                record.last_order_time = False
                record.last_date_str = False
            return

        last_ordered_products = {}

        if order_type == 'sale':
            last_ordered_products = self._get_last_sold_products(partner_id)

        for record in self:
            last_date = last_ordered_products.get(record.id)

            record.last_order_time = last_date if last_date else False
            record.last_date_str = self._get_time_ago_string(last_date) if last_date else False

    def _get_last_sold_products(self, partner_id):
        '''Fetch products last sold to the given customer'''

        sale_order_lines = self.env['sale.order.line'].search([
            ('order_id.partner_id', '=', partner_id)
        ])

        if not sale_order_lines:
            return {}

        invoices = self.env['account.move'].search([
            ('partner_id', '=', partner_id),
            ('invoice_origin', 'in', sale_order_lines.order_id.mapped('name'))
        ])

        last_sale_ordered_products = {}
        invoice_dates = {inv.invoice_origin: inv.create_date for inv in invoices}
        for sol in sale_order_lines:
            last_date = invoice_dates.get(sol.order_id.name)
            if last_date:
                product_id = sol.product_id.product_tmpl_id.id
                if product_id not in last_sale_ordered_products or last_date > last_sale_ordered_products[product_id]:
                    last_sale_ordered_products[product_id] = last_date

        return last_sale_ordered_products

    def _get_time_ago_string(self, last_date):
        '''Convert datetime to human-readable time difference (e.g., "1d", "4h", "4mo")'''

        if not last_date:
            return ""

        now = fields.Datetime.now()
        diff = now - last_date

        if diff.days > 365:
            return f"{diff.days // 365}y"
        elif diff.days > 30:
            return f"{diff.days // 30}mo"
        elif diff.days > 0:
            return f"{diff.days}d"
        elif diff.seconds >= 3600:
            return f"{diff.seconds // 3600}h"
        elif diff.seconds >= 60:
            return f"{diff.seconds // 60}m"
        else:
            return f"{diff.seconds}s"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        '''Modify product dropdown in sale order line to show last sold date'''

        domain = args or []
        partner_id = self.env.context.get('partner_id')
        order_type = self.env.context.get('order_type')
        active_id = self.env.context.get('active_id')
        if active_id:
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

            products = sorted(products, key=lambda p: p.last_order_time if p.last_order_time else datetime.min, reverse=True)

            return [(product.id, product.display_name, product.last_date_str if product.last_date_str else False) for product in products]

        return super().name_search(name, args, operator, limit)

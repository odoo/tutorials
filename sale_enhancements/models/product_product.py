from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ProductProduct(models.Model):
    _inherit = "product.product"
    
    def _compute_time_difference(self, past_date, current_date):
        """Compute relative time difference for display."""
        delta = relativedelta(current_date, past_date)
        if delta.years > 0:
            return f"{delta.years} year(s) ago"
        elif delta.months > 0:
            return f"{delta.months} month(s) ago"
        elif delta.days > 0:
            return f"{delta.days} day(s) ago"
        elif delta.hours > 0:
            return f"{delta.hours} hour(s) ago"
        elif delta.minutes > 0:
            return f"{delta.minutes} minute(s) ago"
        return "Just now"
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """Show last-invoiced products first for the customer in the dropdown."""
        args = args or []
        partner_id = self._context.get("partner_id")
        if not partner_id:
            return super().name_search(name, args, operator, limit)
        original_results = super().name_search(name, args, operator, limit=None)
        if not original_results:
            return []
        product_ids = [res[0] for res in original_results]
        products = self.browse(product_ids)
        invoice_lines = self.env['account.move.line'].search([
            ('partner_id', '=', partner_id),
            ('product_id', 'in', product_ids),
            ('move_id.move_type', '=', 'out_invoice'),
            ('move_id.state', '=', 'posted')
        ])
        product_last_invoice = {}
        for line in invoice_lines:
            product_id = line.product_id.id
            last_date = line.move_id.invoice_date
            if product_id not in product_last_invoice or last_date > product_last_invoice[product_id]:
                product_last_invoice[product_id] = last_date
        now = fields.Datetime.now()
        def sort_key(product):
            last_date = product_last_invoice.get(product.id)
            if last_date:
                return (0, last_date, product.display_name)
            return (1, None, product.display_name)
        sorted_products = sorted(products, key=sort_key)
        result = []
        for product in sorted_products:
            display_name = product.display_name
            last_date = product_last_invoice.get(product.id)
            if last_date:
                last_datetime = fields.Datetime.to_datetime(last_date)
                time_diff = self._compute_time_difference(last_datetime, now)
                display_name += f" ({time_diff})"
            result.append((product.id, display_name))
        if limit:
            result = result[:limit]
        return result

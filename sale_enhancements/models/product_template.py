from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _compute_time_difference(self, past_date, current_date):
        """Compute relative time difference for display."""
        delta = relativedelta(current_date, past_date)
        if delta.years > 0:
            return f"{delta.years} Yr"
        elif delta.months > 0:
            return f"{delta.months} Mo"
        elif delta.days > 0:
            return f"{delta.days} D"
        elif delta.hours > 0:
            return f"{delta.hours} H"
        elif delta.minutes > 0:
            return f"{delta.minutes} Min"
        return "Just now"
    
    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = args or []
        partner_id = self._context.get("partner_id")
        if not partner_id:
            return super().name_search(name, args, operator, limit)
        search_domain = args
        if name:
            search_domain += [("name", operator, name)]
        products = self.search(search_domain, limit=None)
        if not products:
            return []
        product_variants = self.env["product.product"].search([
            ("product_tmpl_id", "in", products.ids)
        ])
        now = fields.Datetime.now()
        invoice_lines = self.env["account.move.line"].search([
            ("product_id", "in", product_variants.ids),
            ("partner_id", "=", partner_id),
            ("move_id.move_type", "=", "out_invoice"),
            ("move_id.state", "=", "posted"),
        ],
            order="create_date DESC",
        )
        product_invoice_dates = {}
        for line in invoice_lines:
            tmpl_id = line.product_id.product_tmpl_id.id
            date = line.move_id.create_date
            if tmpl_id not in product_invoice_dates or product_invoice_dates[tmpl_id] < date:
                product_invoice_dates[tmpl_id] = date
        invoiced_products = []
        non_invoiced_products = []
        for product in products:
            if product.id in product_invoice_dates:
                invoiced_products.append(product)
            else:
                non_invoiced_products.append(product)
        invoiced_products.sort(key=lambda p: product_invoice_dates[p.id], reverse=True)
        non_invoiced_products.sort(key=lambda p: p.name)
        sorted_products = invoiced_products + non_invoiced_products
        result = []
        for product in sorted_products:
            display_name = product.name
            last_date = product_invoice_dates.get(product.id)
            if last_date:
                time_diff = self._compute_time_difference(last_date, now)
                display_name += f" ({time_diff})"
            result.append((product.id, display_name))
        if limit:
            result = result[:limit]
        return result

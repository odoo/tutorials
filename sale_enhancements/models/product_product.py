from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_time_difference(self, past_date, current_date):
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

        now = fields.Datetime.now()

        invoice_lines = self.env["account.move.line"].search([
            ("product_id", "in", products.ids),
            ("partner_id", "=", partner_id),
            ("move_id.move_type", "=", "out_invoice"),
            ("move_id.state", "=", "posted"),
        ])

        product_invoice_dates = {}
        for line in invoice_lines:
            pid = line.product_id.id
            date = line.move_id.create_date
            if pid not in product_invoice_dates or product_invoice_dates[pid] < date:
                product_invoice_dates[pid] = date

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
            display_name = product.display_name
            last_date = product_invoice_dates.get(product.id)
            if last_date:
                time_diff = self._compute_time_difference(last_date, now)
                display_name += f" ({time_diff})"
            result.append((product.id, display_name))

        if limit:
            result = result[:limit]
        return result

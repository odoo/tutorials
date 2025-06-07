from datetime import date
from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        '''Modify product dropdown in sale order line to show last sold product'''

        args = args or []
        partner_id = self._context.get("partner_id")
        last_sold_data = self._get_last_sold_data(partner_id)

        if not partner_id or not last_sold_data:
            return super().name_search(name, args, operator, limit)

        last_sold_template_ids = list(last_sold_data.keys())

        last_sold_products = self.search(
            [("id", "in", last_sold_template_ids), ("name", operator, name)] + args,
            limit=limit
        )

        other_products = self.search(
            [("id", "not in", last_sold_template_ids), ("name", operator, name)] + args,
            limit=limit - len(last_sold_products)
        )

        sorted_last_sold = sorted(last_sold_products, key=lambda p: last_sold_template_ids.index(p.id))

        result = []
        for product in list(sorted_last_sold) + list(other_products):
            lead_time_str = ""
            if product.id in last_sold_data:
                days_ago = (date.today() - last_sold_data[product.id]).days
                lead_time_str = self._format_days_ago(days_ago)
            name_display = f"{product.display_name} ({lead_time_str})" if lead_time_str else product.display_name
            result.append((product.id, name_display))

        return result

    def _get_last_sold_data(self, partner_id):
        invoice_lines = self.env["account.move.line"].search(
            [
                ("move_id.partner_id", "=", partner_id),
                ("move_id.state", "=", "posted"),
                ("move_id.move_type", "in", ["out_invoice", "out_receipt", "out_refund"]),
                ("product_id.product_tmpl_id", "!=", False),
            ],
            order="invoice_date desc, move_id.id desc, id asc"
        )

        last_sold_data = {}
        for line in invoice_lines:
            tmpl_id = line.product_id.product_tmpl_id.id
            if tmpl_id not in last_sold_data and line.move_id.invoice_date:
                last_sold_data[tmpl_id] = line.move_id.invoice_date
        return last_sold_data

    def _format_days_ago(self, days):
        if days == 0:
            return "today"
        elif days == 1:
            return "1 day ago"
        elif days < 30:
            return f"{days} days ago"
        elif days < 365:
            months = days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        else:
            years = days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"

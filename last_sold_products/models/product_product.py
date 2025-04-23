from datetime import date
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    last_invoice_time = fields.Char(string="Last Invoice Time", compute="_compute_last_invoiced")

    def _compute_last_invoiced(self):
        for product in self:
            active_model = self.env.context.get("active_model")
            partner_id = None
            move_types = []

            if active_model == "sale.order.line":
                current_order = self.env["sale.order"].browse(self.env.context.get("order_id"))
                partner_id = current_order.partner_id.id
                move_types = ["out_invoice", "out_receipt", "out_refund"]

            elif active_model == "purchase.order.line":
                current_order = self.env["purchase.order"].browse(self.env.context.get("order_id"))
                partner_id = current_order.partner_id.id
                move_types = ["in_invoice", "in_receipt", "in_refund"]

            else:
                product.last_invoice_time = ""
                continue

            partner_invoice_dates = self._get_last_invoice_data(partner_id, move_types)

            invoice_date = partner_invoice_dates.get(product.id)
            if invoice_date:
                days_ago = (date.today() - invoice_date).days
                product.last_invoice_time = self._format_days_ago(days_ago)
            else:
                product.last_invoice_time = ""

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        '''Modify product dropdown in purchase order line to show last purchased product'''

        args = args or []
        partner_id = self._context.get("partner_id")
        move_type = ["in_invoice", "in_receipt", "in_refund"]
        last_purchased_data = self._get_last_invoice_data(partner_id, move_type)

        if not partner_id or not last_purchased_data:
            return super().name_search(name, args, operator, limit)

        last_purchased_product_ids = list(last_purchased_data.keys())

        last_purchased_products = self.search(
            [("id", "in", last_purchased_product_ids), ("name", operator, name)] + args,
            limit=limit
        )

        other_products = self.search(
            [("id", "not in", last_purchased_product_ids), ("name", operator, name)] + args,
            limit=limit - len(last_purchased_products)
        )

        sorted_last_purchased = sorted(last_purchased_products, key=lambda p: last_purchased_product_ids.index(p.id))

        result = []
        for product in list(sorted_last_purchased) + list(other_products):
            lead_time_str = ""
            if product.id in last_purchased_data:
                days_ago = (date.today() - last_purchased_data[product.id]).days
                lead_time_str = self._format_days_ago(days_ago)
            name_display = f"{product.display_name} ({lead_time_str})" if lead_time_str else product.display_name
            result.append((product.id, name_display))

        return result

    def _get_last_invoice_data(self, partner_id, move_type):
        purchase_lines = self.env["account.move.line"].search(
            [
                ("move_id.partner_id", "=", partner_id),
                ("move_id.state", "=", "posted"),
                ("move_id.move_type", "in", move_type),
                ("product_id", "!=", False),
            ],
            order="invoice_date desc"
        )

        last_purchased_data = {}
        for line in purchase_lines:
            product_id = line.product_id.id
            if product_id not in last_purchased_data and line.move_id.invoice_date:
                last_purchased_data[product_id] = line.move_id.invoice_date
        return last_purchased_data

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

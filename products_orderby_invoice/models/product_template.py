from odoo import models, fields, api
from datetime import date


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = list(args) if args else []
        partner_id = self.env.context.get("partner_id")
        results = []
        matched_ids = []

        lines = self.env["account.move.line"].search([
                ("move_id.move_type", "=", "out_invoice"),
                ("move_id.partner_id", "=", partner_id),
                ("move_id.state", "=", "posted"),
                ("product_id.product_tmpl_id", "!=", False),
            ])

        lines = sorted(
            lines, key=lambda l: l.move_id.invoice_date or fields.Date.today(),
            reverse=True)

        tmpl_map = {}
        for line in lines:
            tmpl = line.product_id.product_tmpl_id
            if tmpl.id not in tmpl_map:
                tmpl_map[tmpl.id] = {"tmpl": tmpl, "date": line.move_id.invoice_date}
            if len(tmpl_map) >= limit:
                break

        name_lower = name.lower() if name else ""
        today = date.today()

        for info in tmpl_map.values():
            tmpl = info["tmpl"]
            invoice_date = info["date"]
            if not name or (operator == "ilike" and name_lower in tmpl.name.lower()):
                days = (today - invoice_date).days if invoice_date else "?"
                display = f"{tmpl.display_name} (Last ordered {days} days ago)"
                results.append((tmpl.id, display))
                matched_ids.append(tmpl.id)
            if len(results) >= limit:
                break

        remaining = limit - len(results)
        if remaining > 0:
            domain = args[:]
            if name:
                domain.append(("name", operator, name))
            if matched_ids:
                domain.append(("id", "not in", matched_ids))
            others = super().name_search(name, args=domain, operator=operator, limit=remaining)
            results.extend(others)

        return results

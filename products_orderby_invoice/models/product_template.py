# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = list(args) if args else []
        partner_id = self.env.context.get("partner_id")
        results = []
        seen_ids = set()

        if partner_id:
            lines = self.env["account.move.line"].search([
                ("move_id.move_type", "=", "out_invoice"),
                ("move_id.partner_id", "=", partner_id),
                ("move_id.state", "=", "posted"),
                ("product_id.product_tmpl_id", "!=", False),
            ])
            lines = sorted(lines, key=lambda l: l.move_id.invoice_date or fields.Date.today(), reverse=True)

            for line in lines:
                tmpl = line.product_id.product_tmpl_id
                if tmpl.id in seen_ids:
                    continue
                days = line.product_id.product_tmpl_id.sale_delay
                display = f"{tmpl.display_name} (Order Lead time {days} days)"
                results.append((tmpl.id, display))
                seen_ids.add(tmpl.id)
                if len(results) >= limit:
                    break

        remaining = limit - len(results)
        if remaining > 0:
            domain = args[:]
            if name:
                domain.append(("name", operator, name))
            if seen_ids:
                domain.append(("id", "not in", list(seen_ids)))
            others = super().name_search(name, args=domain, operator=operator, limit=remaining)
            results.extend(others)

        return results

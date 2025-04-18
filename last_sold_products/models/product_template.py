from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
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

        return [(product.id, product.display_name) for product in list(sorted_last_sold) + list(other_products)]


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
            product_tmpl_id = line.product_id.product_tmpl_id.id
            if product_tmpl_id not in last_sold_data:
                invoice_date = line.move_id.invoice_date
                if invoice_date:
                    last_sold_data[product_tmpl_id] = invoice_date
        return last_sold_data

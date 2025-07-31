from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    last_invoice_date = fields.Date(
        string="Last Invoice Date",
        related='product_variant_id.last_invoice_date',
        store=False
    )
    last_invoice_time_diff = fields.Char(
        string="Last Invoice Time Diff",
        related='product_variant_id.last_invoice_time_diff',
        store=False
    )

    product_variant_id = fields.Many2one(
        'product.product',
        compute='_compute_product_variant_id',
        store=True,
        index=True
    )

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = args or []

        partner_id = self.env.context.get('sale_order_partner_id') \
            or self.env.context.get('purchase_order_partner_id')
        if not partner_id:
            return super().name_search(name, args, operator, limit)

        is_sale = bool(self.env.context.get('sale_order_partner_id'))
        recent_lines = self.env['product.product']._get_recent_invoices(
            partner_id=partner_id,
            is_sale=is_sale
        )

        if not recent_lines:
            return super().name_search(name, args, operator, limit)

        recent_template_ids = list(dict.fromkeys(
            self.env['product.product'].browse(rl['pid']).product_tmpl_id.id
            for rl in recent_lines
        ))

        base_domain = [('name', operator, name)] + args

        recent_templates = self.search(
            [('id', 'in', recent_template_ids)] + base_domain,
            limit=limit
        )
        other_templates = self.search(
            [('id', 'not in', recent_template_ids)] + base_domain,
            limit=max(0, limit - len(recent_templates))
        )

        results = []
        for tmpl_id in recent_template_ids:
            tmpl = recent_templates.filtered(lambda t: t.id == tmpl_id)
            if tmpl:
                td = tmpl.last_invoice_time_diff
                label = f"{tmpl.display_name} ⏱ {td}" if td else tmpl.display_name
                results.append((tmpl.id, label))

        results.extend((t.id, t.display_name) for t in other_templates)
        return results

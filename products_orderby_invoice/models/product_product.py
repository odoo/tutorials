# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    surplus_qty = fields.Float(string='Surplus Quantity', compute='_compute_surplus_qty')
    invoice_date = fields.Datetime(string='Last Invoice Date', compute='_compute_invoice_date')

    @api.depends('invoice_date')
    def _compute_invoice_date(self):
        for rec in self:
            lines = self.env['account.move.line'].search([
                ('product_id', '=', rec.id),
                ('move_id.move_type', '=', 'out_invoice'),
                ('move_id.state', '=', 'posted'),
            ], limit=1, order='date desc')
            rec.invoice_date = lines.move_id.date if lines else False

    @api.depends('virtual_available', 'qty_available')
    def _compute_surplus_qty(self):
        for rec in self:
            rec.surplus_qty = rec.qty_available - rec.virtual_available

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = list(args) if args else []
        partner_id = self.env.context.get('partner_id')
        results = []
        matched_ids = set()

        if partner_id:
            lines = self.env['account.move.line'].search([
                ('move_id.move_type', '=', 'out_invoice'),
                ('move_id.partner_id', '=', partner_id),
                ('move_id.state', '=', 'posted'),
                ('product_id', '!=', False),
            ])

            lines = sorted(lines, key=lambda l: l.move_id.invoice_date or l.create_date, reverse=True)

            for line in lines:
                product = line.product_id
                if product.id in matched_ids:
                    continue
                results.append((product.id, product.display_name))
                matched_ids.add(product.id)
                if len(results) >= limit:
                    break

        remaining = limit - len(results)
        if remaining > 0:
            domain = args[:]
            if name:
                domain.append(('name', operator, name))
            if matched_ids:
                domain.append(('id', 'not in', list(matched_ids)))
            others = super().name_search(name, domain, operator=operator, limit=remaining)
            results.extend(others)

        return results

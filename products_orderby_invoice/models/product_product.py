from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'


    surplus_qty = fields.Float(string='Surplus Quantity', compute='_compute_surplus_qty')

    @api.depends('virtual_available', 'qty_available')
    def _compute_surplus_qty(self):
        for rec in self:
            rec.surplus_qty = rec.qty_available - rec.virtual_available

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        print("===============This is triggered====================")
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

            name_lower = name.lower() if name else ''

            for line in lines:
                product = line.product_id
                if product.id in matched_ids:
                    continue
                if not name or (operator == 'ilike' and name_lower in product.name.lower()):
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
                domain.append(('id', 'not in', list(matched_ids)))  # needs to be a list here
            others = super().name_search(name, domain, operator=operator, limit=remaining)
            results.extend(others)

        return results

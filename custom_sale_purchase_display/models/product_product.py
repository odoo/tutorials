from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    last_invoice_date = fields.Date(
        string="Last Invoice Date",
        compute="_compute_last_invoice_data",
        store=False
    )
    last_invoice_time_diff = fields.Char(
        string="Last Invoice Time Diff",
        compute="_compute_last_invoice_data",
        store=False
    )

    def _compute_last_invoice_data(self):
        for product in self:
            partner_id = product.env.context.get('sale_order_partner_id') \
                or product.env.context.get('purchase_order_partner_id')

            is_sale = bool(product.env.context.get('sale_order_partner_id'))
            move_type = 'out_invoice' if is_sale else 'in_invoice'

            domain = [
                ('state', '=', 'posted'),
                ('invoice_date', '!=', False),
                ('line_ids.product_id', '=', product.id),
                ('move_type', '=', move_type),
            ]
            if partner_id:
                domain.append(('partner_id', '=', partner_id))

            move = product.env['account.move'].search(
                domain, order='invoice_date desc', limit=1
            )

            product.last_invoice_date = move.invoice_date if move else False
            product.last_invoice_time_diff = (
                self._format_time_diff(move.invoice_date) if move else False
            )

    @api.model
    def _get_recent_invoices(self, partner_id, is_sale=True):
        if not partner_id:
            return []

        move_type = 'out_invoice' if is_sale else 'in_invoice'
        moves = self.env['account.move'].search([
            ('partner_id', '=', partner_id),
            ('move_type', '=', move_type),
            ('state', '=', 'posted'),
            ('invoice_date', '!=', False)
        ], order='invoice_date desc')

        recent, seen = [], set()
        for mv in moves:
            for line in mv.line_ids.filtered('product_id'):
                pid = line.product_id.id
                if pid not in seen:
                    recent.append({'pid': pid, 'date': mv.invoice_date})
                    seen.add(pid)
        return recent

    @api.model
    def _format_time_diff(self, invoice_date):
        if not invoice_date:
            return ""
        days = (fields.Date.today() - invoice_date).days
        if days > 365:
            return f"{days // 365}y ago"
        if days > 30:
            return f"{days // 30}mo ago"
        if days > 7:
            return f"{days // 7}w ago"
        if days > 0:
            return f"{days}d ago"
        return "today"

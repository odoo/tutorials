from odoo import models, fields, api
from datetime import datetime


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Computed stock-related fields to be shown per product line
    forecasted_qty = fields.Float(string="Forecasted Qty", compute='_compute_forecasted_qty', store=False)
    qty_on_hand = fields.Float(string="On Hand Qty", compute='_compute_qty_on_hand', store=False)
    qty_difference = fields.Float(string="Qty Difference", compute='_compute_qty_difference', store=False)

    @api.depends('product_id')
    def _compute_forecasted_qty(self):
        """Fetches forecasted quantity (virtual stock) for selected product."""
        for line in self:
            if line.product_id:
                line.forecasted_qty = line.product_id.virtual_available
            else:
                line.forecasted_qty = 0.0

    @api.depends('product_id')
    def _compute_qty_on_hand(self):
        """Fetches current on-hand quantity for selected product."""
        for line in self:
            if line.product_id:
                line.qty_on_hand = line.product_id.qty_available
            else:
                line.qty_on_hand = 0.0

    @api.depends('forecasted_qty', 'qty_on_hand')
    def _compute_qty_difference(self):
        """Computes difference between forecasted and on-hand quantity."""
        for line in self:
            line.qty_difference = line.forecasted_qty - line.qty_on_hand


# Inherit SaleOrder to display last sold products for a customer
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Computed list of recent products sold to the selected customer
    last_sold_products = fields.Many2many(
        'product.product',
        compute='_compute_last_sold_products',
        string="Last 5 Sold Products"
    )

    # Last invoice date for the selected customer
    last_invoice_date = fields.Date(
        compute='_compute_last_invoice_date',
        string="Last Invoice Date"
    )

    # Textual info summary of last sold products and invoice timestamps
    last_sold_products_info = fields.Text(
        compute='_compute_last_sold_products_info',
        string="Last Sold Products Info"
    )

    # Used to conditionally hide info block if there's no history
    invisible_last_sold_info = fields.Boolean(
        compute='_compute_invisible_last_sold_info',
        string="Hide Last Sold Info"
    )

    @api.depends('partner_id')
    def _compute_last_sold_products(self):
        """
        Retrieves unique products from posted customer invoices,
        ordered by invoice date for selected partner.
        """
        for order in self:
            if not order.partner_id:
                order.last_sold_products = [(5, 0, 0)]
                continue

            # Search for invoice lines with products for the customer
            lines = self.env['account.move.line'].search([
                ('move_id.partner_id', '=', order.partner_id.id),
                ('move_id.move_type', '=', 'out_invoice'),
                ('move_id.state', '=', 'posted'),
                ('display_type', '=', 'product'),
                ('product_id', '!=', False)
            ], order='date desc, id desc')

            # Deduplicate products to keep the latest 5 sold ones
            product_ids_ordered = []
            seen_products = set()
            for line in lines:
                if line.product_id.id not in seen_products:
                    product_ids_ordered.append(line.product_id.id)
                    seen_products.add(line.product_id.id)

            order.last_sold_products = [(6, 0, product_ids_ordered)]

    @api.depends('partner_id')
    def _compute_last_invoice_date(self):
        """
        Finds the most recent invoice date for this customer.
        """
        for order in self:
            if not order.partner_id:
                order.last_invoice_date = False
                continue

            last_invoice = self.env['account.move'].search([
                ('partner_id', '=', order.partner_id.id),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('invoice_date', '!=', False)
            ], order='invoice_date desc', limit=1)

            order.last_invoice_date = last_invoice.invoice_date if last_invoice else False

    @api.depends('last_sold_products', 'partner_id')
    def _compute_last_sold_products_info(self):
        """
        Generates readable lines like:
        • Product A (Invoiced 3 days ago on 2024-06-15)
        """
        for order in self:
            if not order.last_sold_products:
                order.last_sold_products_info = "No recent products found for this customer."
                continue

            product_ids = order.last_sold_products.ids
            last_invoice_dates = {}

            # Find invoice dates per product
            all_lines = self.env['account.move.line'].search([
                ('move_id.partner_id', '=', order.partner_id.id),
                ('product_id', 'in', product_ids),
                ('move_id.move_type', '=', 'out_invoice'),
                ('move_id.state', '=', 'posted'),
                ('move_id.invoice_date', '!=', False)
            ])

            for line in all_lines:
                product_id = line.product_id.id
                invoice_date = line.move_id.invoice_date
                if product_id not in last_invoice_dates or invoice_date > last_invoice_dates.get(product_id):
                    last_invoice_dates[product_id] = invoice_date

            info_lines = []
            current_dt = fields.Datetime.now()

            for product in order.last_sold_products:
                last_date = last_invoice_dates.get(product.id)
                if last_date:
                    # Time difference from now to last invoice date
                    invoice_dt = datetime.combine(last_date, datetime.min.time())
                    time_diff = current_dt - invoice_dt
                    days = time_diff.days

                    if days > 1:
                        time_str = f"{days} days ago"
                    elif days == 1:
                        time_str = "1 day ago"
                    else:
                        time_str = f"{time_diff.seconds // 3600} hours ago"

                    info_lines.append(f"• {product.display_name} (Invoiced {time_str} on {last_date.strftime('%Y-%m-%d')})")
                else:
                    info_lines.append(f"• {product.display_name} (No recent invoice found)")

            order.last_sold_products_info = "\n".join(info_lines)

    @api.depends('last_sold_products')
    def _compute_invisible_last_sold_info(self):
        """Boolean toggle: hide info block if no products available."""
        for order in self:
            order.invisible_last_sold_info = not bool(order.last_sold_products)

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_printable_kit = fields.Boolean(
        string="Print Kit in Report",
        default=False,
        help="If checked, kit products will be printed in the report."
    )

    has_kit = fields.Boolean(
        string="Has Kit Product",
        compute="_compute_has_kit",
        store=True,
        default=False,
    )

    @api.depends('order_line', 'order_line.is_kit')
    def _compute_has_kit(self):
        for order in self:
            order.has_kit = any(line.is_kit for line in order.order_line)

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order.
        """
        invoice_vals = super()._prepare_invoice()
        # Copy the value of your toggle to the invoice
        invoice_vals['is_printable_kit'] = self.is_printable_kit
        return invoice_vals

    def _create_invoices(self, grouped=False, final=False, date=None):
        # First, create the invoice(s) using the standard Odoo method.
        # This will include lines for the main product and all sub-products.
        invoices = super()._create_invoices(grouped, final, date)

        # Now, loop through the newly created invoices to apply your logic
        for invoice in invoices:
            # Check the toggle copied from the Sale Order
            if not invoice.is_printable_kit:

                # Find all invoice lines that came from a sale order line
                # marked as a sub-product.
                sub_product_invoice_lines = invoice.invoice_line_ids.filtered(
                    lambda line: line.sale_line_ids and line.sale_line_ids[0].is_subproduct
                )

                # If any sub-product lines were found, delete them
                if sub_product_invoice_lines:
                    sub_product_invoice_lines.unlink()

        return invoices

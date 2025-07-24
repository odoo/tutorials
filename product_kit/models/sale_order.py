from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_printable_kit = fields.Boolean(
        related="order_line.is_kit",
        string="Is Printable Kit",
        readonly=False,
        store=True
    )

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

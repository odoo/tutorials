import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True)

    def action_sold(self):
        """ Override action_sold to create an empty invoice when selling a property. """
        # Call the original method to keep its behavior
        res = super().action_sold()

        for property in self:
            if not property.buyer_id:
                raise UserError("A buyer must be assigned before marking the property as sold.")

            # Find the default Sales Journal
            journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
            if not journal:
                raise UserError("No sales journal found! Please configure one.")

            # Line 1: 6% of the property selling price
            line1_vals = {
                'name': 'Property Sale Commission (6%)',
                'quantity': 1,
                'price_unit': property.selling_price * 0.06,  # 6% of selling price
                'account_id': journal.default_account_id.id,  # Use the default account of the journal
            }

            # Line 2: Administrative Fee of 100
            line2_vals = {
                'name': 'Administrative Fee',
                'quantity': 1,
                'price_unit': 100.00,  # Administrative fee
                'account_id': journal.default_account_id.id,  # Use the default account of the journal
            }

            # Step 2: Create an empty invoice (Customer Invoice)
            invoice_vals = {
                'partner_id': property.buyer_id.id,  # The buyer (customer)
                'move_type': 'out_invoice',  # Type: Customer Invoice
                'journal_id': journal.id,  # Use the found sales journal
                # Step 3: Add invoice lines
                'invoice_line_ids': [(0, 0, line1_vals), (0, 0, line2_vals)]
            }
            invoice = self.env['account.move'].create(invoice_vals)
            # Link the invoice to the property
            property.invoice_id = invoice.id

        return res

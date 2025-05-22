from datetime import datetime

from odoo import Command, models


class EstateProperty(models.Model):
    """Model extending the 'estate.property' model to add invoicing functionality.

    This model overrides the 'action_sold' method to create an invoice in the accounting
    module ('account.move') when a property is marked as sold. It prepares invoice data
    including the property's selling price and administrative fees.
    """

    _inherit = "estate.property"

    def action_sold(self):
        """Mark the property as sold and create an invoice.

        Extends the parent 'action_sold' method to create an invoice in the accounting
        module after the property is successfully marked as sold. Ensures the user has
        write access before proceeding.
        """
        self.check_access("write")
        if super().action_sold() is True:
            invoice_vals = self._prepare_invoice()
            self.env["account.move"].sudo().create(invoice_vals)

    def _prepare_invoice(self):
        """Prepare invoice data for the sold property.

        Creates a dictionary of values for an 'account.move' invoice, including the buyer,
        invoice date, and line items for the property commission (6% of selling price)
        and administrative fees.
        """
        invoice_vals = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_date": datetime.today(),
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": self.name,
                        "quantity": 1,
                        "price_unit": (self.selling_price * 0.06),
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100,
                    }
                ),
            ],
        }
        return invoice_vals

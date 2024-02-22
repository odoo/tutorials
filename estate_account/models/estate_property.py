from odoo import Command, models


class EstatePropertyInvoice(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        invoice_vals_list = list()
        for order in self:
            invoice_lines = [
                Command.create(
                    {
                        "name": "6% of the selling price",
                        "price_unit": order.selling_price * 0.06,
                        "quantity": 1,
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative Fees",
                        "price_unit": 100,
                        "quantity": 1}
                ),
            ]

            invoice_vals = {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": invoice_lines,
            }

            invoice_vals_list.append(invoice_vals)

        self.env["account.move"].sudo().with_context(
            default_move_type="out_invoice"
        ).create(invoice_vals_list)
        return super().action_sold_property()

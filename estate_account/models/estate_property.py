from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        invoices_vals = []

        for record in self:
            invoices_vals.append({
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": f"Commission (6%) - {record.name}",
                        "quantity": 1,
                        "price_unit": 0.06 * record.selling_price,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100.00,
                    }),
                ],
            })

        if invoices_vals:
            self.env["account.move"].with_context(default_move_type="out_invoice").create(invoices_vals)
        return res

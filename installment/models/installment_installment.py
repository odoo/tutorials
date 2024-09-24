from datetime import timedelta
import logging
from odoo import api, Command, models, fields


class Installment(models.Model):
    _name = "installment.installment"

    @api.model
    def _cron_create_invoice(self):
        today = fields.Date.today()
        config_param = self.env["ir.config_parameter"]
        delay_penalty_process = int(
            config_param.get_param(
                "installment.delay_penalty_process", default=0)
        )
        invoices = self.env["account.move"].search([
            ("move_type", "=", "out_invoice"),
            ("state", "=", "posted"),
            ("payment_state", "=", "not_paid"),
            ("penalty_applied", "=", False),
            (
                "invoice_date_due",
                "<=",
                today - timedelta(days=delay_penalty_process),
            ),
        ])
        for invoice in invoices:
            list = self._calculate_penalty(invoice.amount_total)
            for line in invoice.line_ids:
                if (line.product_id.id == self.env.ref("installment.product_installment").id):
                    sale_order = self.env["sale.order"].search(
                        [("invoice_ids", "=", invoice.id)]
                    )
                    # print(sale_order.name)
                    values = {
                        "move_type": "out_invoice",
                        "partner_id": invoice.partner_id.id,
                        "invoice_date": fields.Date.today(),
                        "penalty_applied": True,
                        "invoice_line_ids": [
                            Command.create(
                                {
                                    "name": "Installment included total amount",
                                    "product_id": self.env.ref(
                                        "installment.product_installment"
                                    ).id,
                                    "price_unit": invoice.amount_total,
                                    "quantity": 1.0,
                                    "tax_ids": None,
                                }
                            ),
                            Command.create(
                                {
                                    "name": f"Penalty imposed {list[2]} % on total amount.",
                                    "product_id": self.env.ref(
                                        "installment.due_penalty"
                                    ).id,
                                    "price_unit": list[0],
                                    "quantity": 1.0,
                                    "tax_ids": None,
                                }
                            ),
                        ],
                    }
                    new_invoice = self.env["account.move"].create(values)
                    new_invoice.action_post()
                    sale_order.order_line.invoice_lines = [
                        Command.set(new_invoice.line_ids.ids)
                    ]
                    invoice.write(
                        {
                            "penalty_applied": True,
                        }
                    )
                else:
                    continue

    def _calculate_penalty(self, amount_total):
        """
        Calculated a penalty based on the invoice total And
        Return the list[ penatly amount, due process day, percentage ]
        """
        config_param = self.env["ir.config_parameter"]
        delay_penalty_percentage = int(
            config_param.get_param(
                "installment.delay_penalty_percentage", default=0)
        )
        delay_penalty_process = int(
            config_param.get_param(
                "installment.delay_penalty_process", default=0)
        )
        float_delay_penalty_percentage = delay_penalty_percentage / 100
        return [
            amount_total * float_delay_penalty_percentage,
            delay_penalty_process,
            delay_penalty_percentage,
        ]

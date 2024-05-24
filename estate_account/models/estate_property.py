from odoo import models, fields


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        invoice_lines_val = [
            (
                0,
                0,
                {
                    "name": self.name + " - Down Payment (6%)",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                },
            ), (
                0,
                0,
                {
                    "name": "Administrative Fee",
                    "quantity": 1,
                    "price_unit": 100.00,
                },
            )
        ]

        self.env["account.move"].sudo().with_context(
            default_move_type='out_invoice',
            default_company_id=self.env.company.id,
            default_invoice_date=fields.Date.today()
        ).create(
            {
                "partner_id": self.buyer.id,
                "invoice_line_ids": invoice_lines_val,
            }
        )

        return super().action_set_sold()

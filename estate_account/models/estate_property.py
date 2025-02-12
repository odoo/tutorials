from odoo import Command, models
from odoo.exceptions import AccessError, ValidationError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        try:
            self.check_access("write")
        except AccessError:
            raise AccessError(
                "You do not have the necessary permissions to mark this property as sold."
            )
        
        if not self.partner_id:
            raise ValidationError(
                "Please define a buyer for the property before marking it as sold."
            )
        if not self.selling_price:
            raise ValidationError(
                "Selling price must be set before marking the property as sold."
            )

        current_company = self.env.company

        sell_journal = self.env["account.journal"].search(
            [("name", "=", "Sell"), ("company_id", "=", current_company.id)], limit=1
        )

        if not sell_journal:
            sell_journal = self.env["account.journal"].create({
                "name": "Sell",
                "type": "sale",
                "code": "SELL",
                "company_id": current_company.id,
            })

        invoice_vals = {
            "partner_id": self.partner_id.id,
            "move_type": "out_invoice",
            "journal_id": sell_journal.id,
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": "Commission (6% of Selling Price)",
                        "quantity": 1,
                        "price_unit": self.selling_price * 0.06,
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative Fee",
                        "quantity": 1,
                        "price_unit": 100.00,
                    }
                ),
            ],
        }

        self.env["account.move"].sudo().create(invoice_vals)
        return super(EstateProperty, self).action_sold()


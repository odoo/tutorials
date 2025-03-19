from odoo import api, Command, fields, models
from odoo.exceptions import UserError, AccessError


class estateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.check_access("write")

        company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,  # Defaults to the current user's company
    )
        result = super().action_sold()

        # journal = self.env["account.journal"].sudo().search([("type", "=", "sale")], limit=1)
        # if not journal:
        #     raise UserError("No sales journal found!")

        if not self.buyer_id:
            raise UserError("No buyer is assigned to this property!")

        invoice ={
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                # "journal_id": journal.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Property Sale Commision",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }
        
        try:
            self.env["account.move"].check_access_rights("create")
        except AccessError:
            raise UserError("You do not have the required permissions to create invoices.")

        self.env["account.move"].sudo().create(invoice)

        return result

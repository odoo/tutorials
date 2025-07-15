from odoo import models, Command
from odoo.exceptions import UserError


class Estate(models.Model):
    _inherit = 'estate.property'

    def action_mark_sold(self):
        self.check_access('write')
        res = super().action_mark_sold()

        journal = self.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
        if not journal:
            raise UserError("No sale journal found. Please configure at least one sale journal.")

        for record in self:
            if not record.buyer:
                raise UserError("Please set a Buyer before generating an invoice.")
            if not record.selling_price:
                raise UserError("Please set a Selling Price before generating an invoice.")

            invoice_vals = {
                "partner_id": record.buyer.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    Command.create({
                        "name": "6% Commission",
                        "quantity": 1,
                        "price_unit": 0.06 * record.selling_price,
                    }),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.0,
                    }),
                ]
            }

            self.env["account.move"].sudo().create(invoice_vals)

        return res

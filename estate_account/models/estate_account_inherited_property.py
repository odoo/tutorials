from odoo import Command, models
from odoo.exceptions import AccessError, UserError


class Property(models.Model):
    _inherit = "estate.property"

    def _get_default_journal(self):
        journal_type = self.env.context.get('journal_type', 'sale')
        return self.env['account.journal'].search([
            *self.env['account.journal']._check_company_domain(self.env.company),
            ('type', '=', journal_type),
        ], limit=1)

    def action_sell_property(self):
        # check for permissions
        try:
            self.env["account.move"].check_access('create')
        except AccessError:
            raise UserError("You do not have the correct rights")

        # if no buyer, do not invoice
        if self.buyer_id is None:
            return super().action_sell_property()

        MOVE_TYPE = "out_invoice"
        # get journal
        journal = self._get_default_journal()

        # create invoice lines
        invoice_line_ids = [
            Command.create({
                "name": "Selling price percentage",
                "quantity": 1,
                "price_unit": self.selling_price * 0.06,
            }),
            Command.create({
                "name": "Administrative fees",
                "quantity": 1,
                "price_unit": 100.00,
            }),
        ]

        # create the invoice values object
        invoice_vals = {
            "move_type": MOVE_TYPE,
            "journal_id": journal.id,
            "partner_id": self.buyer_id.id,
            "invoice_line_ids": invoice_line_ids,
        }

        # make the invoice
        self.env["account.move"].sudo().with_context(
            default_move_type=MOVE_TYPE).create(invoice_vals)

        # invoke the parent functionality
        return super().action_sell_property()

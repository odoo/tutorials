from odoo import _, models, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        res = super().action_set_sold()

        if not self:
            return res

        for property in self:
            if not property.buyer_id:
                raise UserError(_("Cannot create invoice: Buyer is not set for property"))

            if property.selling_price <= 0:
                raise UserError(_("Cannot create invoice: Selling price must be positive for property"))

            commission = property.selling_price * 0.06
            admin_fees = 100.00

            invoice_line_commands = [
                Command.create({
                    'name': '6% Commission',
                    'quantity': 1,
                    'price_unit': commission,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': admin_fees,
                }),
            ]

            invoice_vals = {
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': invoice_line_commands,
            }

            self.env['account.move'].create(invoice_vals)

        return res

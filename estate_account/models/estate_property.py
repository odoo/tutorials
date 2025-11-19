# Odoo Imports
from odoo import _, Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    # -----------------------------
    # Inherited Action Methods
    # -----------------------------
    def action_sold(self):
        """
        Extends the base `action_sold` method to generate a customer invoice
        upon property sale. Includes commission and administrative fees.
        """
        res = super().action_sold()

        for property in self:
            if not property.buyer_id:
                raise UserError(_("Please set a buyer before generating an invoice."))

            invoice_vals = {
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'ref': f"Property Sale: {property.name}",
                'invoice_line_ids': [
                    Command.create({
                        'name': property.name,
                        'quantity': 1,
                        'price_unit': property.selling_price,
                    }),
                    Command.create({
                        'name': _('6%% Commission'),
                        'quantity': 1,
                        'price_unit': 0.06 * property.selling_price,
                    }),
                    Command.create({
                        'name': _('Administrative Fees'),
                        'quantity': 1,
                        'price_unit': 100.0,
                    }),
                ]
            }

            self.env['account.move'].create(invoice_vals)
        return res

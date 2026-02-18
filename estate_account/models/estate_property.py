from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        super().action_set_sold()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)

        for property in self:
            commission = 0.06 * property.selling_price

            self.env['account.move'].sudo().create({
                'name': property.name,
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': f"Commission for selling property {property.name}",
                        'quantity': 1,
                        'price_unit': commission,
                    }),
                    Command.create({
                        'name': "Administrative fees",
                        'quantity': 1,
                        'price_unit': 100.0,
                    }),
                ],
            })
        return True

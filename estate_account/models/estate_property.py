from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_mark_sold(self):
        for record in self:
            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': "out_invoice",
                'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,
                'invoice_line_ids': [
                    Command.create({
                        "name": f"Brokerage fees for property {record.name}",
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": f"Administrative fees for property {record.name}",
                        "quantity": 1,
                        "price_unit": 100.0,
                    }),
                ],
            })
        return super().action_mark_sold()
    
from odoo import fields, models

class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def action_sell_property(self):
        # Get default sales journal for now
        sales_journal = self.env['account.journal'].search(
            [
                ('type', '=', 'sale')
            ], 
            limit = 1
        ).id

        for property in self:
            self.env['account.move'].create({
                'partner_id': property.partner_id.id,
                'journal_id': sales_journal,
                'move_type': 'out_invoice',
                'invoice_line_ids': [fields.Command.create({
                        'name': 'Tax',
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06
                    }), fields.Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100
                    })],
            })

        return super().action_sell_property()

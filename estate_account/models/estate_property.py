from odoo import models, Command


class EstateInvoice(models.Model):
    _inherit = 'estate.property'

    def sell_action(self):
        print("Inherited model for invocing is working fine")
        self.check_access('write')
        print(" reached ".center(100, '='))
        self.env['account.move'].sudo().create(
            {
                'partner_id': self.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': self.name,
                        'quantity': 1,
                        'price_unit': self.selling_price*0.06
                    }),

                    Command.create({
                        'name': self.name,
                        'quantity': 1,
                        'price_unit': self.selling_price+100.00
                    })]
            }
        ).action_post()

        return super().sell_action()
        

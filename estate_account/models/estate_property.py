from odoo import models,Command,_
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _description='Real estate property invoicing model'
    _inherit='estate.property'

    def action_mark_as_sold(self):
        try:
            self.check_access('write')
            self.env['account.move'].sudo().create({
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                Command.create({
                    "name": "Charges",
                    "quantity": 1,
                    "price_unit": self.selling_price,
                    }),
                Command.create({
                    "name": "Additional Charges",
                    "quantity": 1,
                    "price_unit": 0.06 * self.selling_price,
                    }),
                Command.create({
                    "name": "Additional Fees",
                    "quantity": 1,
                    "price_unit": 100.00
                    })
                ]
            })

        except Exception as e:
            raise UserError("You don't have the correct accesses to create invoice")

        finally:
            return super().action_mark_as_sold()

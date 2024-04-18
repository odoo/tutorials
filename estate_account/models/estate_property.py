from odoo import models, Command

class InheritedProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold_property(self):
        move_dict = {
            'partner_id': super().buyer.id,
            'move_type': 'out_invoice',
            'journal_id': 1,
            "invoice_line_ids": [
                Command.create({
                    "name": super().name,
                    "quantity": 1,
                    "price_unit": super().selling_price*0.06,
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100,
                })
            ],
        }
        move = self.env['account.move'].create(move_dict)
        return super().action_set_sold_property()

from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        self.env['account.move'].create(
            {
                "partner_id": self.partner_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({'name': '6 percent selling price', 'quantity': 1, 'price_unit': self.selling_price*0.06}),
                    Command.create({'name': 'Administrative fees', 'quantity': 1, 'price_unit': 100.00})
                ]
            }
        )
        
        return super().sell_property()

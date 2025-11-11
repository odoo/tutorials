from odoo import models, Command


class EstateProperty(models.Model):
    _inherit="estate.property"
    
    def action_sold(self):
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                    Command.create(
                        {
                            "name": "6% of the selling price",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06 ,
                        }
                    ),
                    Command.create(
                        {
                            "name": "An additional 100 from administrative fees",
                            "quantity": 1,
                            "price_unit": 100,
                        }
                    )
                ],
            })
        return super().action_sold()

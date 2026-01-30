from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def action_mark_as_sold(self):
        super().action_mark_as_sold()
        for record in self:
            if record.state == 'cancelled':
                continue
                
            self.env['account.move'].create({
                "partner_id": record.buyer_id.id, 
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create({
                        "name": "6% of selling price",
                        "quantity": 1,
                        "price_unit": 0.06 * record.selling_price
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100
                    })
                ]
            })
        return True

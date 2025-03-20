from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    def action_sold(self):
        res = super(EstateProperty, self).action_sold()

        moves_to_create = []
        for property in self:
            moves_to_create.append({
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                'invoice_line_ids': [
                    Command.create({
                        'name': "Commission (6%)",
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': "Administrative Fees",
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            })

        self.env["account.move"].create(moves_to_create)

        return res
    
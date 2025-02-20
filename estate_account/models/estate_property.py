from odoo import models, Command


class InheritedProperty(models.Model):
    _inherit = "estate.property"

    def sold_property(self):
        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(
            {
                'partner_id' : int(self.buyer_id),
                "line_ids" : [
                    Command.create({
                        "name" : "6% of selling price",
                        "quantity" : 1,
                        "price_unit" : self.selling_price * 0.06
                    }),
                    Command.create({
                        "name": "administrative fees",
                        "quantity": 1,
                        "price_unit": 100.0
                    })
                ],
             }
        )
        return super().sold_property()
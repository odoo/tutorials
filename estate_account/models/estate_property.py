from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit="estate.property"

    def action_do_sold(self):
        # call super method for confirmation property sold or not??
        res = super(EstateProperty, self).action_do_sold()

        invoice = self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": 'out_invoice',
                "line_ids": [
                    Command.create({
                        "name": self.name,
                        "quantity":1,
                        "price_unit": self.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "administrative fees",
                        "quantity":1,
                        "price_unit": 100,
                    })
                ]
            }
        )
        return res

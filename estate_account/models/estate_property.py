from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit="estate.property"

    def action_do_sold(self):
        # call super method for confirmation property sold or not??
        res = super(EstateProperty, self).action_do_sold()

        # Ensure user has 'write' access to the property
        self.check_access('write', raise_exception=True)

        print(" reached ".center(100, '='))

        invoice = self.env["account.move"].sudo().create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": 'out_invoice',
                "line_ids": [
                    Command.create({
                        "name": self.name + "(6% of selling price)",
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

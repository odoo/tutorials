from odoo import models, Command

class InheritedEstateProperty(models.Model):
    _inherit = "estate.property"


    def action_sold_adv(self):
        self._create_property_invoice()
        return super().action_sold_adv()

    def _create_property_invoice(self):
        for property in self:
            self.env["account.move"].with_context(default_move_type='out_invoice').create({
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": "6% fee",
                        "quantity": 1,
                        "price_unit": property.selling_price * 0.06
                    }),
                    Command.create({
                        "name": "Admnistrative fee",
                        "quantity": 1,
                        "price_unit": 100
                    })
                ]
            })

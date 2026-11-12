from odoo import models
from odoo.orm.commands import Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        super().action_sold_property()

        self.env["account.move"].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create(
                    {
                        'name': '6% of selling price',
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06,
                    },
                ),
                Command.create(
                    {
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100
                    }
                )
            ]
        })

        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Congratulation! This property has been sold',
                'img_url': '/web/image/%s/%s/image_1024' % (self.buyer_id.id,
                                                            self.salesperson_id.id) if self.buyer_id.image_1024 else '/web/static/img/smile.svg',
                'type': 'rainbow_man',
            }
        }

from odoo import Command
from odoo import models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        for property in self:
            if not property.buyer_id:
                raise UserError(_("can't sell because buyer is not set"))

            self.env['account.move'].create({
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': "Down Payment",
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': "Administrative Fee",
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ]
            })

        return super().action_set_sold()

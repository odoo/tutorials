from odoo import models, Command, _
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("This property has already been sold."))
            if not record.selling_price:
                raise UserError(_("cannot sell a property before accepting an offer"))
            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Commission(%6)',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            })
        return super().action_sold()

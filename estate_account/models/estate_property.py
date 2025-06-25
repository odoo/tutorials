from odoo import _, Command, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        self.check_access('write')
        for record in self:
            if not record.buyer_id:
                raise UserError(_("Buyer is not set for this property"))
            invoice_vals = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': "Service Fee(6%)",
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': "Administrative Fee",
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ]
            }
            invoice = self.env['account.move'].sudo().create(invoice_vals)
        return super().action_sold()

from odoo import fields, models, Command


class estate_property(models.Model):
    _inherit = "estate.property"

    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True)

    def action_sold(self):
        self.check_access('write')
        invoice = self.env['account.move'].sudo().create({
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            "invoice_origin": self.name,
            'date': fields.Date.today(),
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price,
                    'account_id': self.env['account.account'].search([('deprecated', '=', False)], limit=1).id,
                }),
                Command.create({
                    'name': '6 percent of Selling Price',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                    'account_id': self.env['account.account'].sudo().search([('deprecated', '=', False)], limit=1).id,
                }),
                Command.create({
                    'name': 'Administrative Fee',
                    'quantity': 1,
                    'price_unit': 100.0,
                    'account_id': self.env['account.account'].sudo().search([('deprecated', '=', False)], limit=1).id,
                }),
            ]
        })
        self.invoice_id = invoice
        return super().action_sold()

    def show_invoice(self):
        return {
        'type': 'ir.actions.act_window',
        'name': 'Invoice',
        'res_model': 'account.move',
        'view_mode': 'form',
        'res_id': self.invoice_id.id,
        'target': 'current',
        }

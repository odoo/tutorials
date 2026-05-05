from odoo import Command, fields, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    account_move_ids = fields.One2many('account.move', 'estate_property_id', string="Invoices", tracking=True)

    def action_set_sold(self):
        sold = super().action_set_sold()
        for rec in self:
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': rec.buyer_id.id,
                'estate_property_id': rec.id,
                'invoice_line_ids': [
                    Command.create({'name': "%s Selling Price" % rec.name, 'quantity': 1, 'price_unit': rec.selling_price}),
                    Command.create({'name': 'Commission (6%)', 'quantity': 1, 'price_unit': rec.selling_price * 0.06}),
                    Command.create({'name': 'Administrative Fees', 'quantity': 1, 'price_unit': 100}),
                ]
            })
        return sold

    def action_open_invoice(self):
        invoice = self.account_move_ids[:1]
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }

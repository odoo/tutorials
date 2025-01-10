from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_order_id = fields.Many2one('sale.order')
    penalty_invoice_id = fields.Many2one('account.move')
    is_penalty_applied = fields.Boolean(string="Penalty Applied")

    def action_open_penalty_invoices(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Penalty invoices',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', '=', self.penalty_invoice_id.id)], 
            'target': 'current',
        }


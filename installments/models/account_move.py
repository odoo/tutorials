from odoo import models,fields, api, Command
class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_order_id=fields.Many2one('sale.order')
    penalty_invoice_id=fields.Many2one('account.move')
    penalty_applied = fields.Boolean(string="Penalty Applied", default=False)

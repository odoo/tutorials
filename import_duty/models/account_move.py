from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_duty_enabled = fields.Boolean(
        related='company_id.custom_duty',
        store=False,
        readonly=True,
    )

    on_confirm = fields.Boolean(default=False)

    bill_of_entry_move_id = fields.Many2one(
        'account.move', string="Bill of Entry Journal Entry", readonly=True)

    def action_open_bill_of_entry_wizard(self):
        return {
            'name': 'Bill of Entry Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'bill.of.entry',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_vendor_bill_id': self.id,
            },
        }

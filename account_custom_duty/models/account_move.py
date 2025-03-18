from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_duty_journal_entry_id = fields.Many2one('account.move', string='Journal Entry of Custom Duty', readonly=True)

    def action_open_bill_of_entry_wizard(self):
        self.ensure_one()
        if self.state != 'posted' or self.l10n_in_gst_treatment not in ['overseas', 'special_economic_zone', 'deemed_export']:
            raise UserError('Action can only be performed on posted moves with GST treatment like overseas, special economic zone, or deemed export .')
        return {
            'name': 'Bill of Entry',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'bill.entry.wizard',
            'view_id': self.env.ref('account_custom_duty.bill_entry_wizard_view_form').id,
            'target': 'new',
            'context': {
                'move_id': self.id 
            },
        }

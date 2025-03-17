from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_journal_entry_custom_duty = fields.Many2one(
        'account.move', readonly=True
    )

    def action_l10n_in_custom_duty_wizard(self):
        self.ensure_one()
        if self.state != 'posted' or self.l10n_in_gst_treatment not in ['overseas', 'special_economic_zone', 'deemed_export']:
            raise UserError(_('This action can only be performed on posted moves with overseas, special economic zone, or deemed export GST treatment.'))
        return {
            'name': _('Custom Duty Entry'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'l10n_in.custom.duty.wizard',
            'view_id': self.env.ref('l10n_in_custom_duty.bill_entry_wizard_view_form').id,
            'target': 'new',
            'context': {
                'move_id': self.id
            },
        }

    def action_l10n_in_bill_of_entry(self):
        self.ensure_one()
        if not self.l10n_journal_entry_custom_duty:
            raise UserError(_('No custom duty entry found for this move.'))
        return {
            'name': _("Bill of Entry"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_id': self.l10n_journal_entry_custom_duty.id,
        }

# imports of odoo
from odoo import api, fields, models


class Project(models.Model):
    _inherit = 'project.project'

    is_sync_required = fields.Boolean(compute="_compute_is_sync_required", string="Is sync required?")
    move_lines = fields.One2many('account.move.line', compute="_compute_is_sync_required", string="Move lines")

    # Method returns account move lines (invoice lines) that needs synchronization.
    def _get_sync_required_move_lines(self):
        return self.env['account.move.line'].search([
            ('move_id', 'in', self.sale_order_id.invoice_ids.ids),
            ('date_changed', '!=', self.date_start),
            ('move_type', '!=', 'entry'),
            ('parent_state', '=', 'posted'),
            ('account_internal_group', 'in', ['income', 'expense'])
        ])

    # Computes if synchronization is required based on related invoices and start date.
    @api.depends('sale_order_id.invoice_ids', 'date_start')
    def _compute_is_sync_required(self):
        self.move_lines = self._get_sync_required_move_lines()
        self.is_sync_required = bool(self.move_lines)

    def open_recognition_date_sync_wizard(self):
        """
        Open the recognition date synchronization wizard for related account move lines.

        This method prepares the context with the relevant move line IDs and
        date and action values before launching the
        `account.account_automatic_entry_wizard_action` wizard.
        """
        action = self.env.ref('account.account_automatic_entry_wizard_action').read()[0]

        # Force the values of the move line in the context to avoid issues
        ctx = dict(self.env.context)
        ctx.pop('active_ids', None)
        ctx.pop('default_journal_id', None)
        ctx['active_ids'] = self.move_lines.ids
        ctx['active_model'] = 'account.move.line'
        ctx['default_action'] = 'change_period'
        ctx['default_date'] = self.date_start

        action['context'] = ctx
        return action

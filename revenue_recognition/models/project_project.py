from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    has_unrecognized_entries = fields.Boolean(
        string="Has Unrecognized Entries",
        compute='_compute_has_unrecognized_entries',
        store=False,
    )

    unrecognized_entries_message = fields.Char(
        string="Unrecognized Entries Message",
        compute='_compute_unrecognized_entries_message',
    )

    @api.depends('date_start', 'sale_order_id')
    def _compute_has_unrecognized_entries(self):
        for project in self:
            project.has_unrecognized_entries = False

            if not project.sale_order_id or not project.date_start:
                continue

            invoices = project.sale_order_id.invoice_ids

            if not invoices:
                continue

            generated_entries = self.env['account.move'].search([
                ('adjusting_entry_origin_move_ids', 'in', invoices.ids)
            ])

            has_current_recognition = generated_entries.filtered(
                lambda m: m.date == project.date_start
            )
            project.has_unrecognized_entries = not bool(has_current_recognition)

    @api.depends('has_unrecognized_entries', 'date_start')
    def _compute_unrecognized_entries_message(self):
        for project in self:
            if project.has_unrecognized_entries and project.date_start:
                project.unrecognized_entries_message = (
                    f"You still have journal items that need to be recognised "
                    f"from {project.date_start.strftime('%m/%d/%Y')}"
                )
            else:
                project.unrecognized_entries_message = False

    def _get_original_invoice_lines(self, move_lines):
        generated_entries = move_lines.filtered(
            lambda l: bool(l.move_id.adjusting_entry_origin_move_ids)
        )

        if not generated_entries:
            return move_lines.filtered(
                lambda l: l.account_id.account_type == 'income'
            )

        origin_moves = generated_entries.mapped('move_id.adjusting_entry_origin_move_ids')

        invoice_lines = self.env['account.move.line'].search([
            ('move_id', 'in', origin_moves.ids),
            ('parent_state', '=', 'posted'),
        ])

        return invoice_lines.filtered(
            lambda l: l.account_id.account_type == 'income'
        )

    def action_recognize_invoices(self):
        self.ensure_one()

        if not self.account_id:
            return False

        move_lines = self.env['account.move.line'].search([('parent_state', '=', 'posted')]).filtered(lambda l: l.analytic_distribution and str(self.account_id.id) in l.analytic_distribution)

        original_invoice_lines = self._get_original_invoice_lines(move_lines)

        if not original_invoice_lines:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Journal Items',
                    'message': 'No journal items found for this project.',
                    'type': 'warning',
                    'sticky': False,
                }
            }

        return {
            'name': 'Create Automatic Entries',
            'type': 'ir.actions.act_window',
            'res_model': 'account.automatic.entry.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_model': 'account.move.line',
                'active_ids': original_invoice_lines.ids,
                'project_id': self.id,
                'default_action': 'change_period',
            },
        }

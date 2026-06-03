from odoo import models, fields


class AccountAutomaticEntryWizard(models.TransientModel):
    _inherit = 'account.automatic.entry.wizard'

    date = fields.Date(
        required=True,
        default=lambda self: self._get_default_date(),
        readonly=False
    )

    def do_action(self):
        project_id = self.env.context.get('project_id')

        if not project_id:
            return super().do_action()

        project = self.env['project.project'].browse(project_id)
        invoices = project.sale_order_id.invoice_ids

        draft_entries = self.env['account.move'].search([
            ('adjusting_entry_origin_move_ids', 'in', invoices.ids),
            ('state', '=', 'draft'),
        ])

        if not draft_entries:
            return super().do_action()
        latest_draft = draft_entries.sorted(key=lambda m: m.create_date, reverse=True)[:1]
        latest_draft.write({'date': self.date})
        old_drafts = draft_entries - latest_draft
        if old_drafts:
            old_drafts.unlink()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': latest_draft.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def _get_default_date(self):
        project_id = (self.env.context.get('project_id') or self.env.context.get('create_for_project_id'))
        if project_id:
            project = self.env['project.project'].browse(project_id)
            if project.exists() and project.date_start:
                return project.date_start
        if self.env.context.get('active_model') == 'account.move.line':
            for line in self.env['account.move.line'].browse(
                self.env.context.get('active_ids', [])):
                if line.analytic_distribution:
                    for analytic_id_str in line.analytic_distribution:
                        try:
                            project = self.env['project.project'].search([('account_id', '=', int(analytic_id_str))], limit=1)
                            if project and project.date_start:
                                return project.date_start
                        except (ValueError, TypeError):
                            pass

        return fields.Date.context_today(self)

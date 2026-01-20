from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    date_reloaded = fields.Date(string="Reloaded Date")

    def action_automatic_entry(self, default_action=None):
        action = super().action_automatic_entry(default_action)
        ctx = dict(action.get('context', {}))

        project = self.move_id.line_ids.sale_line_ids.order_id.project_id
        if project and project.date_start:
            ctx['default_date'] = project.date_start

        action['context'] = ctx

        return action

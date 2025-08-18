# imports of odoo
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    date_changed = fields.Date(string="Changed Date")

    def action_automatic_entry(self, default_action=None):
        """
        If account move line is linked to a saled order that is
        connected to a project with a defined start date, that date
        is set as default date in wizard context.
        """
        action = super().action_automatic_entry(default_action)
        ctx = dict(action.get('context', {}))

        project = self.move_id.line_ids.sale_line_ids.order_id.project_id
        if project and project.date_start:
            ctx['default_date'] = project.date_start

        action['context'] = ctx
        return action

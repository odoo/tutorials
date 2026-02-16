from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    recognition_date = fields.Date(
        string="Recognition Date",
        help="Reloaded date from Planned date of corresponding project of sale order",
    )

    def action_automatic_entry(self, default_action=None):
        result = super().action_automatic_entry(default_action)

        ctx = dict(result.get("context", {}))

        project = self.move_id.line_ids.mapped(
            "sale_line_ids.order_id.project_id"
        ).filtered(lambda p: p.date_start)

        if project:
            ctx["default_date"] = project[0].date_start

        result["context"] = ctx
        return result

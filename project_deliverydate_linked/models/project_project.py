from odoo import api, fields, models
from odoo.exceptions import UserError

class Project(models.Model):
    _inherit = "project.project"

    is_reload_required = fields.Boolean(compute="_compute_is_reload_required", string="Is reload required?")

    @api.depends("sale_order_id.invoice_ids")
    def _compute_is_reload_required(self):
        self.is_reload_required = self.env["account.move.line"].search([
            ("move_id", "in", self.sale_order_id.invoice_ids.ids),
            ("account_id.internal_group", "in", ["income", "expense"]),
            ("parent_state", "=", "posted"),
            ("date_reloaded", "!=", self.date_start)
        ])

    def open_cutoff_wizard(self):
        move_lines = self.env["account.move.line"].search([
            ("move_id", "in", self.sale_order_id.invoice_ids.ids),
            ("account_id.internal_group", "in", ["income", "expense"]),
            ("parent_state", "=", "posted"),
            ("date_reloaded", "!=", self.date_start)
        ])

        if not move_lines:
            raise UserError("No journal items need to be recognized.")

        action = self.env.ref("account.account_automatic_entry_wizard_action").read()[0]
        ctx = self.env.context.copy()
        ctx.update({
            "active_ids": move_lines.ids,
            "active_model": "account.move.line",
            "default_action": "change_period",
            "default_date": self.date_start
        })
        action["context"] = ctx
        return action
    
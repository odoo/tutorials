from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    is_recognition_required = fields.Boolean(compute="_compute_is_recognition_required")

    @api.depends("date_start", "sale_order_id.invoice_ids.line_ids.recognition_date")
    def _compute_is_recognition_required(self):
        for project in self:
            project.is_recognition_required = False

            if not project.sale_order_id or not project.date_start:
                continue

            journal_items = self.env["account.move.line"].search(
                [
                    ("move_id", "in", project.sale_order_id.invoice_ids.ids),
                    ("account_id.internal_group", "in", ["income", "expense"]),
                    ("parent_state", "=", "posted"),
                    ("recognition_date", "!=", project.date_start),
                ],
                limit=1,
            )

            project.is_recognition_required = bool(journal_items)

    def open_cut_off_wizard(self):
        self.ensure_one()

        journal_items = self.env["account.move.line"].search(
            [
                ("move_id", "in", self.sale_order_id.invoice_ids.ids),
                ("account_id.internal_group", "in", ["income", "expense"]),
                ("parent_state", "=", "posted"),
                ("recognition_date", "!=", self.date_start),
            ]
        )

        action = self.env["ir.actions.act_window"]._for_xml_id(
            "account.account_automatic_entry_wizard_action"
        )

        ctx = dict(self.env.context or {})
        ctx.update(
            {
                "active_ids": journal_items.ids,
                "active_model": "account.move.line",
                "default_action": "change_period",
                "default_date": self.date_start,
            }
        )

        action["context"] = ctx
        return action

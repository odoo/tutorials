from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    needs_recognition_sync = fields.Boolean(
        compute="_compute_recognition_sync"
    )

    recognition_sync_message = fields.Char(
        compute="_compute_recognition_sync"
    )

    def _get_recognition_moves(self):
        self.ensure_one()

        sale_order = self.sale_order_id

        if not sale_order:
            return self.env["account.move"]

        invoices = sale_order.invoice_ids

        return invoices.mapped("adjusting_entries_move_ids")

    @api.depends("date_start")
    def _compute_recognition_sync(self):
        for project in self:
            project.needs_recognition_sync = False
            project.recognition_sync_message = False

            if not project.date_start:
                continue

            recognition_moves = project._get_recognition_moves()

            if not recognition_moves:
                continue

            recognition_dates = recognition_moves.mapped("date")

            if project.date_start not in recognition_dates:
                project.needs_recognition_sync = True

                project.recognition_sync_message = (
                    "Revenue recognition entries are not aligned "
                    "with the project start date."
                )

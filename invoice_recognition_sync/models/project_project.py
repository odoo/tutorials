import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _inherit = "project.project"

    needs_recognition_sync = fields.Boolean(
        compute="_compute_recognition_sync",
    )

    recognition_sync_message = fields.Char(
        compute="_compute_recognition_sync",
    )

    def _get_recognition_sync_target_date(self):
        self.ensure_one()
        return self.date_start

    def _get_adjusting_entries(self):
        self.ensure_one()

        sale_orders = (self.sale_order_id | self.reinvoiced_sale_order_id)

        logger.warning("self.sale_order_id ============ %s", self.sale_order_id)
        logger.warning("self.reinvoiced_sale_order_id ============ %s", self.reinvoiced_sale_order_id)
        logger.warning("sale_orders ============ %s", sale_orders)
        if not sale_orders:
            return self.env["account.move"]

        invoice_entries = sale_orders.invoice_ids.adjusting_entries_move_ids

        logger.warning("invoice_entries  --------- %s", invoice_entries.read())

        if not invoice_entries:
            return self.env["account.move"]

        wizard_entries = invoice_entries.adjusting_entries_move_ids
        # logger.warning("wizard_entries ----------------- %s", wizard_entries)
        return invoice_entries | wizard_entries

    @api.depends(
        "date_start",
        "sale_order_id.invoice_ids.adjusting_entries_move_ids.date",
        "sale_order_id.invoice_ids.adjusting_entries_move_ids.adjusting_entries_move_ids.date",
        "reinvoiced_sale_order_id.invoice_ids.adjusting_entries_move_ids.date",
        "reinvoiced_sale_order_id.invoice_ids.adjusting_entries_move_ids.adjusting_entries_move_ids.date",
    )
    def _compute_recognition_sync(self):
        for project in self:
            project.needs_recognition_sync = False
            project.recognition_sync_message = False

            target_date = (
                project._get_recognition_sync_target_date()
            )
            # logger.warning("Target date =========== %s", target_date)
            if not target_date:
                continue

            entries = project._get_adjusting_entries()
            # logger.warning("Entries  ++++++++++ %s", entries)

            if not entries:
                continue

            dates = entries.mapped("date")

            if target_date in dates:
                continue

            project.needs_recognition_sync = True

            count = len(entries)
            # logger.info("Count of date ---------- %s", count)
            project.recognition_sync_message = _(
                "%(count)d revenue recognition entries are not aligned with the project start date (%(date)s).",
                count=count, date=target_date, )

    def action_open_recognition_wizard(self):
        self.ensure_one()

        entries = self._get_adjusting_entries()

        if not entries:
            raise UserError(
                _("No revenue recognition entries found.")
            )

        move_lines = entries.line_ids.filtered(
            lambda line: (
                    line.account_id.account_type == "income"
                    and line.move_id.state == "posted"
                    and not line.reconciled
            )
        )

        if not move_lines:
            raise UserError(
                _(
                    "There are no eligible journal "
                    "items to synchronize."
                )
            )

        return {
            "type": "ir.actions.act_window",
            "name": _("Revenue Recognition"),
            "res_model": "account.automatic.entry.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "active_model": "account.move.line",
                "active_ids": move_lines.ids,
                "default_action": "change_period",
                "default_date": (
                    self._get_recognition_sync_target_date()
                ),
                "invoice_recognition_sync_project_id": self.id,
            },
        }

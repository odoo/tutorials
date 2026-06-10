from odoo import models


class AccountAutomaticEntryWizard(models.TransientModel):
    _inherit = "account.automatic.entry.wizard"

    def default_get(self, fields_list):
        values = super().default_get(fields_list)

        project_id = self.env.context.get("invoice_recognition_sync_project_id")

        if (project_id and "date" in fields_list and not values.get("date")):
            project = (self.env["project.project"].browse(project_id).exists())

            if project: values["date"] = (project._get_recognition_sync_target_date())

        return values

    def do_action(self):
        project_id = self.env.context.get("invoice_recognition_sync_project_id")
        if self.action == "change_period" and project_id:
            project = self.env["project.project"].browse(project_id).exists()
            if project:
                old_entries = project._get_adjusting_entries()
                if old_entries:
                    posted = old_entries.filtered(lambda m: m.state == "posted")
                    draft = old_entries.filtered(lambda m: m.state == "draft")
                    if posted:
                        posted.button_draft()
                    (posted | draft).button_cancel()

        return super().do_action()

from odoo import _, models


class AccountAutomaticEntryWizard(models.TransientModel):
    _inherit = "account.automatic.entry.wizard"

    def default_get(self, fields_list):
        values = super().default_get(fields_list)

        project_id = self.env.context.get("invoice_recognition_sync_project_id")

        if (project_id and "date" in fields_list and not values.get("date")):
            project = (self.env["project.project"].browse(project_id).exists())

            if project:
                values["date"] = project._get_recognition_sync_target_date()

        return values

    def do_action(self):
        project_id = self.env.context.get("invoice_recognition_sync_project_id")
        if self.action == "change_period" and project_id:
            project = self.env["project.project"].browse(project_id).exists()
            if project:
                entries = project._get_adjusting_entries()
                if entries:
                    wizard_entries = entries.filtered("auto_post_origin_id")
                    if wizard_entries:
                        posted = wizard_entries.filtered(lambda m: m.state == "posted")
                        if posted:
                            posted.button_draft()
                        wizard_entries.button_cancel()
                        wizard_entries.unlink()

                    invoice_entries = entries - wizard_entries
                    if invoice_entries:
                        if all(e.date == self.date for e in invoice_entries):
                            return {
                                "type": "ir.actions.act_window",
                                "name": _("Revenue Recognition"),
                                "res_model": "account.move",
                                "view_mode": "list,form",
                                "domain": [("id", "in", invoice_entries.ids)],
                            }
                        posted = invoice_entries.filtered(lambda m: m.state == "posted")
                        if posted:
                            posted.button_draft()
                        invoice_entries.date = self.date
                        if posted:
                            posted._post()
                        return {
                            "type": "ir.actions.act_window",
                            "name": _("Revenue Recognition"),
                            "res_model": "account.move",
                            "view_mode": "list,form",
                            "domain": [("id", "in", invoice_entries.ids)],
                        }

        return super().do_action()

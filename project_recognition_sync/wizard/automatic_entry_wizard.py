from odoo import models


class AutomaticEntryWizard(models.TransientModel):
    _inherit = "account.automatic.entry.wizard"

    def do_action(self):
        active_ids = self.env.context.get("active_ids", [])
        journal_lines = self.env["account.move.line"].browse(active_ids)

        journal_lines.write({"recognition_date": self.date})

        return super().do_action()

from odoo import exceptions, models


class Employee(models.Model):
    _inherit = "hr.employee"

    def action_open_related_tds_declaration(self):
        """Opens the TDS Declarations associated with the current employee."""

        action = self.env["ir.actions.actions"]._for_xml_id("hr_payroll_tds.action_open_declarations")
        target_ids = self.env["hr.tds.declaration.details"].search([("employee_id", "=", self.id)])
        if not target_ids:
            raise exceptions.UserError("No TDS declaration available for current employee.")
        action["views"] = [[False, "list"], [False, "form"]]
        action["domain"] = [("id", "in", target_ids.ids)]

        return action

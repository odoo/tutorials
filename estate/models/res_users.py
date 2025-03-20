from odoo import fields, models
from odoo.exceptions import UserError

class res_users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property","sales_person_ids", string=" ")

    def action_generate_sales_person_report(self):

        report = self.env.ref('estate.res_user_report')
        if not report:
            raise UserError("Report not found.")

        return report.report_action(self)

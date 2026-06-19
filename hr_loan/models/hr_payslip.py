from odoo import models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        res = super().action_payslip_done()
        for rec in self:
            loan = self.env['hr.loan'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('state', 'in', ['approved', 'ongoing'])
            ], limit=1)
            if loan:
                line = loan.loan_ids.filtered(
                    lambda r: not r.paid and r.date <= rec.date_to
                )[:1]
                if line:
                    line.paid = True
                    if loan.state == 'approved':
                        loan.state = 'ongoing'
                    if all(loan.loan_line_ids.mapped('paid')):
                        loan.state = 'closed'
        return res

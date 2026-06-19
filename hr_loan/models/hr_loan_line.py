from odoo import api, fields, models


class HrLoanLine(models.Model):
    _name = 'hr.loan.line'

    hr_loan_id = fields.Many2one('hr.loan', ondelete='cascade', readonly=True)
    date = fields.Date(default=fields.Date.today())
    amount = fields.Float()
    paid = fields.Boolean(default=False)
    status = fields.Selection(
        selection=[
            ('paid', "Paid"),
            ('not_paid', "Not Paid")
        ],
        default='not_paid',
        readonly=True
    )

    def action_pay(self):
        self.paid = True
        self.status = 'paid'
        self.hr_loan_id.total_paid += self.amount
        if self.hr_loan_id.state == 'approved':
            self.hr_loan_id.state = 'ongoing'
        if self.hr_loan_id.state == 'ongoing' and all(self.hr_loan_id.loan_line_ids.mapped('paid')):
            self.hr_loan_id.state = 'closed'

    def action_not_paid(self):
        self.paid = False
        self.status = 'not_paid'
        self.hr_loan_id.total_paid -= self.amount
        if self.hr_loan_id.state == 'ongoing' and not any(self.hr_loan_id.loan_line_ids.mapped('paid')):
            self.hr_loan_id.state = 'approved'
        if self.hr_loan_id.state == 'closed':
            self.hr_loan_id.state = 'ongoing'

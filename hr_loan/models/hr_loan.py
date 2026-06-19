from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class HrLoan(models.Model):
    _name = 'hr.loan'
    _rec_name = 'employee_id'

    _check_loan = models.Constraint(
        'CHECK (loan_amount > 0)',
        'Loan Amount should be greater than zero'
    )

    _check_duration = models.Constraint(
        'CHECK (duration_months > 0)',
        'Duration should be greater than zero'
    )

    employee_id = fields.Many2one('hr.employee', required=True)
    department_id = fields.Many2one(related='employee_id.department_id')
    loan_amount = fields.Float(required=True)
    duration_months = fields.Integer(required=True)
    date_start = fields.Date(default=fields.Date.today(), required=True)
    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('approved', "Approved"),
            ('ongoing', "Ongoing"),
            ('closed', "Closed"),
            ('refused', "Refused")
        ],
        default='draft'
    )
    loan_line_ids = fields.One2many('hr.loan.line', 'hr_loan_id')
    reason = fields.Text()
    total_paid = fields.Float(compute='_compute_total_paid', store=True)
    total_outstanding = fields.Float(compute='_compute_total_outstanding', store=True)
    progress = fields.Float(compute='_compute_progress')
    image_1024 = fields.Image(related="employee_id.image_1024")

    def _generate_loan_lines(self):
        for i in range(self.duration_months):
            self.env['hr.loan.line'].create({
                'hr_loan_id': self.id,
                'date': self.date_start + relativedelta(months=i),
                'amount': self.loan_amount / self.duration_months
            })

    @api.depends('loan_line_ids')
    def _compute_total_paid(self):
        for rec in self:
            rec.total_paid = max(sum(rec.loan_line_ids.filtered('paid').mapped('amount')), 0.0)

    @api.depends('total_paid', 'loan_line_ids')
    def _compute_total_outstanding(self):
        for rec in self:
            rec.total_outstanding = rec.loan_amount - rec.total_paid if rec.loan_amount else 0.0

    @api.depends('total_paid', 'loan_amount')
    def _compute_progress(self):
        for rec in self:
            rec.progress = (rec.total_paid / rec.loan_amount * 100) if rec.loan_amount else 0.0

    def action_approve(self):
        self.state = 'approved'
        self._generate_loan_lines()
        return True

    def action_refuse(self):
        self.state = 'refused'
        return True

    def action_close(self):
        self.state = 'closed'
        return True

    def action_reset(self):
        self.state = 'draft'
        self.loan_line_ids = False
        return True

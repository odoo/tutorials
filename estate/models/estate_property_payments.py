from odoo import models, api, fields, _
from odoo.exceptions import UserError


class EstatePropertyPayments(models.Model):
    _name = "estate.property.payments"
    _description = "Real Estate Property Payments"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    booking_id = fields.Many2one("estate.property.booking", string="Booking ID", required=True)
    amount = fields.Float(string="amount")
    _check_amount_positive = models.Constraint(
        'Check(amount > 0)',
        'amount being payed should be grater than 0',
    )
    payment_date = fields.Datetime()
    due_date = fields.Datetime(string="Due Date")
    installment_no = fields.Integer(string="Installment #")
    payment_type = fields.Selection(related="booking_id.payment_type", store=True, readonly=True)
    payment_method = fields.Selection(
        selection=[
            ('cash', "Cash"),
            ('bank', "Bank"),
            ('transfer', "Transfer"),
            ('cheque', "Cheque"),
        ],
        required=True,
        copy=False,
    )
    status = fields.Selection(
        selection=[
            ('pending', "Pending"),
            ('paid', "Paid"),
            ('overdue', "Overdue"),
            ('cancelled', "Cancelled"),
        ], default='pending',
    )
    remarks = fields.Text(string="Remarks")

    @api.constrains('amount', 'status')
    def _check_amount_paid(self):
        for record in self:
            if record.amount <= 0:
                raise UserError(_("amount of a payment cannot be 0 "))
            if record.status == 'paid':
                balance_before = record.booking_id.remaining_amount + record.amount
                if record.amount > balance_before:
                    raise UserError(_("amount cant be more than remaining amount"))

    @api.onchange('payment_type')
    def _check_payment_type(self):
        if self.payment_type == 'full_payments':
            self.amount = self.booking_id.remaining_amount

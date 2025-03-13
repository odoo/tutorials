from odoo import api, fields, models
from odoo.exceptions import ValidationError

class PaymentLines(models.TransientModel):
    _name = "account.payment.lines"
    _description = "Pay Lines"

    account_payment_register_id = fields.Many2one(comodel_name="account.payment.register")
    partner_id = fields.Many2one(string="Vendor", comodel_name="res.partner", readonly=True)
    name = fields.Char(string="Bill Number", readonly=True)
    memo_id = fields.Char(store=True)
    invoice_date = fields.Date(string="Bill Date", readonly=True)
    amount_residual = fields.Float(string="Total Balance Amount", readonly=True)
    balance_amount = fields.Float(store=True)
    payment_amount = fields.Float(string="Payment Amount")

    @api.constrains("payment_amount")
    def _check_payment_amount(self):
        for record in self:
            if abs(record.payment_amount) > abs(record.balance_amount):
                raise ValidationError('Payment amount cannot exceed the total balance amount.')

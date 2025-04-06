from odoo import api, exceptions, fields, models


class AccountPaymentTermDiscount(models.Model):
    _name = 'account.payment.term.discount'
    _description = 'Payment Term Discounts'

    payment_term_id = fields.Many2one('account.payment.term', string="Payment Term")
    discount_percentage = fields.Float(string='Discount %', help='Early Payment Discount granted for this payment term', default=2.0)
    discount_days = fields.Integer(string='Discount Days', help='Number of days before the early payment proposition expires', default=10)
    early_pay_discount_computation = fields.Selection(
        selection=[
            ("included", "On early payment"),
            ("excluded", "Never"),
            ("mixed", "Always (upon invoice)"),
        ],
        string="Cash Discount Tax Reduction", default="included", store=True, required=True
    )

    @api.constrains('discount_percentage', 'discount_days')
    def _check_positive_values(self):
        for record in self:
            if record.discount_percentage <= 0 or record.discount_percentage > 100:
                raise exceptions.ValidationError("Discount Percentage must be strictly between 0 to 100.")
            if record.discount_days <= 0:
                raise exceptions.ValidationError("Discount Days must be strictly positive.")

    def unlink(self):
        payment_terms = self.mapped('payment_term_id')
        res = super().unlink()

        for payment_term in payment_terms:
            if not payment_term.discount_line_ids and payment_term.early_discount:
                payment_term.write({'early_discount': False})

        return res

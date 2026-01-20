from odoo import models, fields, api


class AccountPaymentTermDiscount(models.Model):
    _name = 'account.payment.term.discount'
    _description = 'Early Payment Discounts'

    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string="Payment Term",
        required=True, ondelete="cascade")
    discount_percentage = fields.Float(
        string='Discount %',
        help='Early Payment Discount granted for this payment term')
    discount_days = fields.Integer(
        string='Discount Days',
        help='Number of days before the early payment proposition expires')
    early_pay_discount_computation = fields.Selection([
            ('included', 'On early payment'),
            ('excluded', 'Never'),
            ('mixed', 'Always (upon invoice)'),
        ],
        string='Cash Discount Tax Reduction',
        readonly=False, store=True,
        default='included',
        compute='_compute_discount_computation')

    info_text1 = fields.Char(
        string="Info1",
        compute="_compute_info_text")
    info_text2 = fields.Char(
        string="Info2",
        compute="_compute_info_text")
    info_text3 = fields.Char(
        string="Info3",
        compute="_compute_info_text")

    @api.depends('payment_term_id.early_payment_discount_ids')
    def _compute_info_text(self):
        for record in self:
            if record == record.payment_term_id.early_payment_discount_ids[0]:
                record.info_text1 = "% if paid in first"
            else:
                record.info_text1 = "% if paid in next"
            record.info_text2 = "days"
            record.info_text3 = "Reduced tax:"

    @api.depends('payment_term_id.company_id')
    def _compute_discount_computation(self):
        for record in self:
            payment_term = record.payment_term_id
            country_code = payment_term.company_id.country_code or self.env.company.country_code
            if country_code == 'BE':
                record.early_pay_discount_computation = 'mixed'
            elif country_code == 'NL':
                record.early_pay_discount_computation = 'excluded'
            else:
                record.early_pay_discount_computation = 'included'

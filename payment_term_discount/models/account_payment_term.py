from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, exceptions, _
from odoo.tools import formatLang, format_date


class AccountPaymentTermInherit(models.Model):
    _inherit = 'account.payment.term'

    early_payment_discount_ids = fields.One2many(
        'account.payment.term.discount', 'payment_term_id',
        string="Early Discount Lines")

    @api.depends('currency_id', 'example_amount', 'example_date', 'line_ids.value', 'line_ids.value_amount', 'line_ids.nb_days', 'early_discount', 'discount_percentage', 'discount_days', 'early_payment_discount_ids')
    def _compute_example_preview(self):
        super()._compute_example_preview()
        for record in self:
            lines = []
            record.example_preview_discount = ""
            currency = record.currency_id
            previous_validity_date = record.example_date
            first = True
            if record.early_discount:
                for epd in record.early_payment_discount_ids:
                    date = format_date(self.env, previous_validity_date + relativedelta(days=epd.discount_days or 0))
                    discount_amount = record._get_amount_due_after_discount_for_epd(record.example_amount, 0.0, epd)
                    if first:
                        line = _(
                            "Early Payment Discount: <b>%(amount)s</b> if paid before <b>%(date)s</b>",
                            amount=formatLang(self.env, discount_amount, currency_obj=currency),
                            date=date,
                        )
                        first = False
                    else:
                        indent = "&nbsp;" * 49
                        line = _(
                            "%(indent)s<b>%(amount)s</b> if paid before <b>%(date)s</b>",
                            indent=indent,
                            amount=formatLang(self.env, discount_amount, currency_obj=currency),
                            date=date,
                        )
                    lines.append(line + "<br/>")
                    previous_validity_date = previous_validity_date + relativedelta(days=epd.discount_days or 0)
            record.example_preview_discount = ''.join(lines)

    @api.constrains('early_payment_discount_ids', 'early_discount')
    def _check_minimum_discount_records(self):
        for record in self:
            if record.early_discount and not record.early_payment_discount_ids:
                raise exceptions.UserError(_(
                    "At least one early payment discount is required."
                    "If you do not want to apply any then disable Early Discount."))

    @api.onchange('early_discount')
    def _onchange_early_payment_discount(self):
        if self.early_discount and not self.early_payment_discount_ids:
            self.early_payment_discount_ids = [(0, 0, {
                'discount_percentage': 2.0,
                'discount_days': 10,
            })]

    def action_add_early_payment_discount(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment.term.discount',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_payment_term_id': self.id,
            }
        }

    def _get_amount_due_after_discount_for_epd(self, total_amount, untaxed_amount, epd):
        self.ensure_one()
        percentage = epd.discount_percentage / 100.0
        if self.early_pay_discount_computation in ('excluded', 'mixed'):
            discount_amount_currency = (total_amount - untaxed_amount) * percentage
        else:
            discount_amount_currency = total_amount * percentage
        return self.currency_id.round(total_amount - discount_amount_currency)

    def _get_last_discount_date(self, date_ref):
        self.ensure_one()
        if not date_ref:
            return None
        total_discount_days = sum(self.early_payment_discount_ids.mapped('discount_days'))
        return date_ref + relativedelta(days=total_discount_days or 0) if self.early_discount else False

    def create_early_payment_discount_id(self):
        for record in self:
            record.early_payment_discount_ids = [(0, 0, {
                'payment_term_id': record.id,
                'discount_percentage': 2.0,
                'discount_days': 10,
            })]

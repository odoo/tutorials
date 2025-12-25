from odoo import api, fields, models


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    discount_line_ids = fields.One2many(
        'account.payment.term.discount', 'payment_term_id',
        string="Discount Lines"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('early_discount') and not vals.get('discount_line_ids'):
                vals['early_discount'] = False
        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            if vals.get('early_discount') or 'discount_line_ids' in vals:
                discount_lines = vals.get('discount_line_ids', record.discount_line_ids)
                if not discount_lines:
                    vals['early_discount'] = False
        return super().write(vals)

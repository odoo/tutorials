from odoo import fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    epd_discount_amount_currency = fields.Monetary(string="EPD Discount Amount")
    epd_days_left = fields.Integer(string="EPD Discount Days")

    def _get_invoice_next_payment_values(self, custom_amount=None):
        values = super()._get_invoice_next_payment_values(custom_amount=custom_amount)

        discount_amount_currency = self.epd_discount_amount_currency
        days_left = self.epd_days_left

        if discount_amount_currency and days_left:
            if days_left > 0:
                values["epd_discount_msg"] = _(
                    "Discount of %(amount)s if paid within %(days)s days",
                    amount=self.currency_id.format(discount_amount_currency),
                    days=days_left,
                )
            else:
                values["epd_discount_msg"] = _(
                    "Act now! Pay today and save %(amount)s!",
                    amount=self.currency_id.format(discount_amount_currency)
                )
        return values

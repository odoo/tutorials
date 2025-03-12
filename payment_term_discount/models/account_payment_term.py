from odoo import models, fields, Command, _


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"
    parent_id = fields.Many2one("account.payment.term", ondelete="cascade")
    early_discount_ids = fields.One2many("account.payment.term", "parent_id", string="Early Payment Discounts")

    def action_add_discount_line(self):
        for record in self:
            record.early_discount_ids = [
                Command.create(
                    {
                        "name": _(f"Child Discount - {record.name}"),
                        "early_discount": True,
                        "early_pay_discount_computation": record.early_pay_discount_computation,
                    }
                )
            ]

from odoo import models, fields, api, Command
from odoo.exceptions import UserError


class AddEmi(models.TransientModel):
    _name = "add.emi"
    total_so_amount = fields.Float(readonly=True)
    down_payment = fields.Float(readonly=True)
    remaining_amount = fields.Float(readonly=True)
    interest = fields.Float(readonly=True)
    number_monthly_installment = fields.Integer(readonly=True)
    installement_amount = fields.Float(readonly=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields) or {}
        active_id = self.env.context["active_id"]
        sale_order = self.env["sale.order"].browse(active_id)
        config_param = self.env["ir.config_parameter"]
        max_duration = float(
            config_param.get_param("installment.max_duration", default=0.0)
        )
        if max_duration == 0:
            raise UserError("Max Duration is zero.")
        down_payment_percentage = int(
            config_param.get_param("installment.down_payment", default=0)
        )
        annual_rate = int(
            config_param.get_param("installment.annual_rate", default=0)
        )

        administrative_expenses = int(
            config_param.get_param("installment.administrative_expenses", default=0.0)
        )
        # Total
        total = sale_order.amount_total
        # Down Payment calculated
        down_payment_evaluate = (down_payment_percentage / 100) * total
        # Administrative Expenses
        remaining = total - down_payment_evaluate
        adminstrative_expense = (administrative_expenses / 100) * remaining
        total_remaining = remaining + adminstrative_expense
        # Annually Interest
        annuall_intrest = ((annual_rate / 100) * total_remaining) * max_duration
        total_remaining += annuall_intrest
        # Installment Amount
        installment_months = max_duration * 12
        installment_ammount = total_remaining / installment_months
        # print(annuall_intrest)
        res.update(
            {
                "total_so_amount": sale_order.amount_total,
                "down_payment": down_payment_evaluate,
                "remaining_amount": sale_order.amount_total - down_payment_evaluate,
                "interest": annuall_intrest,
                "number_monthly_installment": max_duration * 12,
                "installement_amount": installment_ammount,
            }
        )
        return res

    def add_installment(self):
        active_id = self.env.context["active_id"]
        sale_order = self.env["sale.order"].browse(active_id)
        sale_order.order_line = [
            Command.create(
                {
                    "order_id": sale_order.id,
                    "price_unit": self.installement_amount,
                    "product_id": self.env.ref("installment.product_installment").id,
                    "product_uom": self.env.ref("uom.product_uom_unit").id,
                    "tax_id": None,
                }
            ),
            Command.create(
                {
                    "order_id": sale_order.id,
                    "product_uom_qty": 1.0,
                    "price_unit": self.down_payment,
                    "product_id": self.env.ref("installment.product_down_payment").id,
                    "product_uom": self.env.ref("uom.product_uom_unit").id,
                    "tax_id": None,
                },
            ),
        ]
        return

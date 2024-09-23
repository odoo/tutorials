from odoo import api, fields, models


class AddEMIWizard(models.TransientModel):
    _name = "add.emi"
    _description = "Add EMI Wizard"

    total_so_amount = fields.Float(string="Total SO Amount", readonly=True)
    down_payment = fields.Float(string="Down Payment", readonly=True)
    remaining_amount = fields.Float(string="Remaining Amount", readonly=True)
    admin_expenses = fields.Float(string="Admin Expenses", readonly=True)
    interest = fields.Float(string="Interest", readonly=True)
    number_of_installments = fields.Integer(
        string="Number of Monthly Installments", readonly=True
    )
    installment_amount = fields.Float(string="Installment Amount", readonly=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        IrConfigParam = self.env["ir.config_parameter"]
        down_payment_percentage = float(
            IrConfigParam.get_param("installment.down_payment_percentage", default=0)
        )
        annual_rate = float(
            IrConfigParam.get_param("installment.annual_rate", default=0)
        )
        admin_expenses_percentage = float(
            IrConfigParam.get_param("installment.admin_expenses_percentage", default=0)
        )
        max_duration = float(IrConfigParam.get_param("installment.max_duration"))

        sales_order = self.env["sale.order"].browse(self._context.get("active_id"))
        total_amount = sales_order.amount_total
        down_payment = total_amount * (down_payment_percentage / 100)
        remaining_amount = total_amount - down_payment
        admin_expenses = remaining_amount * (admin_expenses_percentage / 100)
        remaining_amount_after_expenses = remaining_amount + admin_expenses
        interest = remaining_amount_after_expenses * (annual_rate / 100) * max_duration
        final_amount = remaining_amount_after_expenses + interest
        if max_duration != 0:
            number_of_installments = max_duration * 12
        else:
            number_of_installments = 1
        installment_amount = final_amount / number_of_installments

        res.update(
            {
                "total_so_amount": total_amount,
                "down_payment": down_payment,
                "remaining_amount": remaining_amount,
                "admin_expenses": admin_expenses,
                "interest": interest,
                "number_of_installments": number_of_installments,
                "installment_amount": installment_amount,
            }
        )
        return res

    def action_add_installment(self):

        sales_order = self.env["sale.order"].browse(self._context.get("active_id"))

        self.env["sale.order.line"].create(
            {
                "name": "Installments",
                "order_id": sales_order.id,
                "product_id": self.env.ref("installment.product_installment").id,
                "product_uom_qty": 1,
                "price_unit": self.installment_amount,
            }
        )
        self.env["sale.order.line"].create(
            {
                "name": "Down Payment",
                "order_id": sales_order.id,
                "product_id": self.env.ref("installment.product_down_payment").id,
                "product_uom_qty": 1,
                "price_unit": self.down_payment,
            }
        )

from odoo import api, Command, fields, models
from odoo.exceptions import UserError


class addEMI(models.TransientModel):
    _name = "add.emi"
    _description = "Add EMI"

    total_amount = fields.Float(string="Total SO Amount", readonly=True)
    down_payment = fields.Float(string="Down Payment", readonly=True)
    remaining_amount = fields.Float(string="Remaining Amount", readonly=True)
    interest = fields.Float(string="Interest", readonly=True)
    number_monthly_installment = fields.Integer(
        string="Number of Monthly Installment", readonly=True
    )
    installment_amount = fields.Float(string="Installment Amount", readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(active_id)
        # print(sale_order.date_order)
        order_line = sale_order.order_line

        max_duration = float(
            self.env["ir.config_parameter"].get_param("installment.max_duration")
        )
        down_payment_rate = float(
            self.env["ir.config_parameter"].get_param("installment.down_payment_percentage")
        )
        annual_percentage_rate = float(
            self.env["ir.config_parameter"].get_param("installment.annual_percentage_rate")
        )
        administrative_expenses_percentage = float(
            self.env["ir.config_parameter"].get_param("installment.administrative_expenses_percentage")
        )

        if max_duration == 0:
            raise UserError(("Max Duration is not defined"))

        # calculate price subtotal

        total_amount = sale_order.amount_total

        # calculate down payment
        down_payment = total_amount * (down_payment_rate / 100)

        # calculate remaining amount
        remaining_amount = total_amount - down_payment
        remaining_amount = remaining_amount + remaining_amount * (
            administrative_expenses_percentage / 100
        )

        # calculate interest
        interest = ((remaining_amount * annual_percentage_rate) / 100) * max_duration

        # calculate number of monthly installment
        number_monthly_installment = max_duration * 12

        # final amount for EMI
        final_amount = remaining_amount + interest

        # Installment amount
        installment_amount = final_amount / number_monthly_installment

        res.update(
            {
                "total_amount": total_amount,
                "down_payment": down_payment,
                "remaining_amount": remaining_amount,
                "interest": interest,
                "number_monthly_installment": number_monthly_installment,
                "installment_amount": installment_amount,
            }
        )
        return res

    def add_Emi_installment(self):

        active_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(active_id)

        sale_order.order_line = [
            Command.create(
                {
                    "name": "installment",
                    "order_id": sale_order.id,
                    "product_id": self.env.ref(
                        "installment.product_product_installment"
                    ).id,
                    "product_uom": 1,
                    "product_uom_qty": 1,
                    "price_unit": self.installment_amount,
                    "tax_id": None,
                }
            ),
            Command.create(
                {
                    "name": "Demo Payment",
                    "order_id": sale_order.id,
                    "product_id": self.env.ref(
                        "installment.product_product_down_payment"
                    ).id,
                    "product_uom": 1,
                    "product_uom_qty": 1,
                    "price_unit": self.down_payment,
                    "tax_id": None,
                }
            ),
        ]

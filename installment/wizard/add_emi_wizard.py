from odoo import models, fields, api


class AddEmi(models.TransientModel):

    _name = "add.emi.button"
    _description = "Add Emi For Installment"

    total_sale_amount = fields.Float(string="Total sale Amount", readonly=True)
    down_payment = fields.Float(compute="_compute_values")
    remaining_amount = fields.Float(compute="_compute_values")
    interest = fields.Float(compute="_compute_values")
    number_of_monthly_installement = fields.Integer(compute="_compute_values")
    installement_amount = fields.Float(readonly=True)
    admin_expense = fields.Float(compute="_compute_values")
    remaining_amount_2 = fields.Float(compute="_compute_values")

    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults["total_sale_amount"] = (
            self.env["sale.order"]
            .browse(self.env.context.get("active_id"))
            .amount_total
        )
        return defaults

    @api.depends("total_sale_amount")
    def _compute_values(self):
        for rec in self:
            down_payment_perc = self.env["ir.config_parameter"].get_param(
                "installment.down_payment_perc"
            )
            x = float(rec.total_sale_amount) * float(down_payment_perc)
            rec.down_payment = x / 100
            rec.remaining_amount = rec.total_sale_amount - rec.down_payment
            administrative_expenses_percentage = self.env[
                "ir.config_parameter"
            ].get_param("installment.administ_exp")
            y = float(rec.remaining_amount) * float(administrative_expenses_percentage)
            rec.admin_expense = y / 100
            rec.remaining_amount_2 = rec.remaining_amount + rec.admin_expense
            max_dur = float(
                self.env["ir.config_parameter"].get_param("installment.max_duration")
            )
            annual_rate_percentage = self.env["ir.config_parameter"].get_param(
                "installment.annual_rate_perc"
            )
            z = (
                float(rec.remaining_amount_2)
                * float(annual_rate_percentage)
                * float(max_dur)
            )
            rec.interest = z / 100
            rec.number_of_monthly_installement = float(max_dur) * 12
            rec.installement_amount = (
                rec.remaining_amount_2 + rec.interest
            ) / rec.number_of_monthly_installement

    # add installment button
    def add_installement(self):
        self.env["sale.order.line"].create(
            [
                {
                    "order_id": self.env.context.get("active_id"),
                    "product_id": self.env.ref("installment.product1").id,
                    "price_unit": self.installement_amount,
                },
                {
                    "order_id": self.env.context.get("active_id"),
                    "product_id": self.env.ref("installment.product2").id,
                    "price_unit": self.down_payment,
                },
            ]
        )

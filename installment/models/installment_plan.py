from odoo import models, fields


class InstallmentPlan(models.Model):
    _name = "installment.plan"
    _description = "Installments info"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order")
    down_payment = fields.Float(string="Down Payment", compute="_compute_down_payment")
    admin_expenses = fields.Float(
        string="Administrative Expenses", compute="_compute_admin_expenses"
    )
    monthly_installment = fields.Float(
        string="Monthly Installment", compute="_compute_monthly_installment"
    )

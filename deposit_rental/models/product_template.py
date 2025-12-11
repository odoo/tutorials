from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    require_deposit = fields.Boolean(string="Require Deposit", help="If Checked, this product requires a deposit.")
    deposit_amount = fields.Monetary(string="Deposit Amount", currency_field="currency_id", store=True, compute="_compute_deposit_amount")

    @api.depends("require_deposit")
    def _compute_deposit_amount(self):
        """ Update deposit amount when 'require_deposit' is checked or deposit product changes in settings """
        deposit_product = self.env["product.product"].sudo().search([
            ("id", "=", self.env["ir.config_parameter"].sudo().get_param("sale_renting.deposit_product_id"))
        ])

        if deposit_product:
            self.filtered("require_deposit").write({"deposit_amount": deposit_product.lst_price})
        else:
            self.write({"deposit_amount": 0.0})

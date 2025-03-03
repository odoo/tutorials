from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    require_deposit = fields.Boolean(string="Require Deposit")
    deposit_amount = fields.Monetary(string="Deposit Amount", currency_field="currency_id", store=True, compute="_compute_deposit_amount")

    @api.depends("require_deposit")
    def _compute_deposit_amount(self):
        deposit_product_id = self.env["ir.config_parameter"].get_param("sale_renting.deposit_product_id")
        deposit_product = self.env["product.product"].browse(int(deposit_product_id))

        for product in self:
            if product.require_deposit and deposit_product:
                product.deposit_amount = deposit_product.lst_price
            else:
                product.deposit_amount = 0.0

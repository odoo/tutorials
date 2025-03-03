from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    deposit_required = fields.Boolean(string="Require Deposit")
    deposit_amount = fields.Float(string="Amount", digits="Product Price", compute="_compute_deposit_amount", store=True)

    @api.depends("deposit_required")
    def _compute_deposit_amount(self):
        deposit_product_id = self.env["ir.config_parameter"].sudo().get_param("deposit_rental.deposit_id")
        deposit_product = self.env["product.product"].sudo().browse(int(deposit_product_id)) if deposit_product_id else None
        for record in self:
            if record.deposit_required and deposit_product and deposit_product.exists():
                record.deposit_amount = deposit_product.lst_price
            else:
                record.deposit_amount = 0.0

    @api.model
    def _update_deposit_amount(self):
        products = self.search([("deposit_required", "=", True)])
        products._compute_deposit_amount()

    def _get_combination_info(self, combination=False, **kwargs):
        res = super()._get_combination_info(combination=combination, **kwargs)
        res.update({
            "deposit_amount": self.deposit_amount,
        })
        return res

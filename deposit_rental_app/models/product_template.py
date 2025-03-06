from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    require_deposit = fields.Boolean(string="Require Deposit")
    amount = fields.Float(string="Deposit Amount")

    def _get_combination_info(
        self, combination=False, product_id=False, add_qty=1.0, **kwargs
    ):
        self.ensure_one()
        combination_info = super()._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, **kwargs
        )
        combination_info["amount"] = self.amount or 0.0
        return combination_info

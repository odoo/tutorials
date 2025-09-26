from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    required_deposit = fields.Boolean(default=False, string="Required Deposit")
    amount = fields.Monetary(string="Amount", default="0.0")

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1.0,
        parent_combination=False,
        only_template=False,
    ):
        combination_info = super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            parent_combination=parent_combination,
            only_template=only_template,
        )

        combination_info.update(
            {
                "required_deposit": self.required_deposit,
                "amount": self.amount,
            }
        )
        return combination_info

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    deposit_product = fields.Boolean(
        string="Deposit Product",
        help="Make it a deposit product.")

    require_deposit = fields.Boolean(
        string="Require Deposit",
        help="Enable if this product requires deposit.")

    deposit_product_amount = fields.Float(
        string="Amount",
        help="This specifies deposit for 1 unit of this product.")

    deposit_quantity = fields.Float(
        string="Deposit Quantity",
        help="Stores the quantity of the product selected in the combination."
    )

    calculated_amount = fields.Float(
        compute = "_compute_calculated_amount"
    )

    @api.depends('deposit_product_amount', 'deposit_quantity')
    def _compute_calculated_amount(self):
        for line in self:
            line.calculated_amount = line.deposit_product_amount * line.deposit_quantity

    def _get_combination_info(
        self, combination=False, product_id=False, add_qty=1.0,
        parent_combination=False, only_template=False,
    ):
        combination_info = super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            parent_combination=parent_combination,
            only_template=only_template,
        )

        self.deposit_quantity = add_qty
        combination_info['calculated_amount'] = self.calculated_amount

        return combination_info

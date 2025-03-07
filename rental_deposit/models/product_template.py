# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    require_deposit = fields.Boolean(
        string='Require Deposit',
    )
    deposit_amount = fields.Float(string="Amount", help="Amount to be deposited per unit of this product")
    deposit_total = fields.Float(compute="_compute_deposit_total")

    @api.constrains('deposit_amount','list_price')
    def _check_deposit_amount(self):
        for product in self:
            if product.deposit_amount <= 0:
                raise ValidationError(_("Deposit amount must be positive when deposit is required."))

    @api.depends('deposit_amount')
    def _compute_deposit_total(self):
        for product in self:
            product.deposit_total = product.deposit_amount

    def _get_combination_info(
        self, combination=False, product_id=False, add_qty=1.0,
        parent_combination=False, only_template=False
    ):
        combination_info = super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            parent_combination=parent_combination,
            only_template=only_template
        )
        combination_info['deposit_total'] = self.deposit_amount * add_qty
        return combination_info

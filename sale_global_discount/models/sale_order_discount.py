# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class SaleOrderDiscount(models.TransientModel):
    _inherit = "sale.order.discount"

    def action_apply_discount(self):
        self.ensure_one()
        company_self = self.with_company(self.company_id)
        if company_self.discount_type == "so_discount":
            company_self.sale_order_id.global_discount_percentage = (company_self.discount_percentage * 100)
            result = super(SaleOrderDiscount, company_self).action_apply_discount()
            company_self.sale_order_id._update_global_discount()
            return result

        return super(SaleOrderDiscount, company_self).action_apply_discount()

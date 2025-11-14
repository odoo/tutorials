from odoo import models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    def _get_applicable_rules_domain(self, products, date, plan_id=None, **kwargs):
        domain = super()._get_applicable_rules_domain(products, date, plan_id, **kwargs)
        if plan_id == 'all':
            domain.append(('plan_id', '!=', False))
        return domain

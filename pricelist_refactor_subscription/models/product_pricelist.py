from odoo import fields, models
from odoo.osv.expression import AND


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    product_subscription_pricelist_ids = fields.One2many(
        comodel_name='product.pricelist.item',
        inverse_name='pricelist_id',
        string="Recurring Pricing Rules",
        domain=lambda self: self._get_subscription_product_domain(),
    )

    def _get_product_domain(self):
        return AND([
            super()._get_product_domain(),
            [('plan_id', '=', False)]
        ])

    def _get_subscription_product_domain(self):
        return AND([
            self._base_product_domain(),
            [('plan_id', '!=', False)]
        ])

    def _get_applicable_rules_domain(self, products, date, plan_id=None, **kwargs):
        domain = super()._get_applicable_rules_domain(products, date, **kwargs)
        if plan_id:
            domain[0] = ('pricelist_id', 'in', [self.id, self.search([], limit=1).id])
            if plan_id != 'all':
                domain.append(('plan_id', '=', plan_id))
        return domain

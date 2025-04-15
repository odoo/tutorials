from odoo import fields, models
from odoo.osv.expression import AND


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    subscription_pricelist_rule_ids = fields.One2many(
        string="Subscription Pricelist Rules",
        comodel_name='product.pricelist.item',
        inverse_name='product_tmpl_id',
        domain=lambda self: self._get_subscription_pricelist_item_domain(),
    )

    def _get_pricelist_item_domain(self):
        return AND([
            super()._get_pricelist_item_domain(),
            [('plan_id', '=', False)]
        ])

    def _get_subscription_pricelist_item_domain(self):
        return AND([
            self._base_pricelist_item_domain(),
            [('plan_id', '!=', False)]
        ])

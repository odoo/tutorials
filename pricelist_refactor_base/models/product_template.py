from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pricelist_rule_ids = fields.One2many(
        string="Pricelist Rules",
        comodel_name='product.pricelist.item',
        inverse_name='product_tmpl_id',
        domain=lambda self: self._base_pricelist_item_domain(),
    )

    def _base_pricelist_item_domain(self):
        """ Return a domain to filter pricelist rules applicable to the given product template(s).

        The domain will filter rules that are either applicable to the product template itself
        or to one of its variants.
        """
        return [
            '|',
            ('product_tmpl_id', 'in', self.ids),
            ('product_id', 'in', self.product_variant_ids.ids),
        ]

    def _get_pricelist_item_domain(self):
        return self._base_pricelist_item_domain()

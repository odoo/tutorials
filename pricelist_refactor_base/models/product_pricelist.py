from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    item_ids = fields.One2many(
        comodel_name='product.pricelist.item',
        inverse_name='pricelist_id',
        string="Pricing Rules",
        domain=lambda self: self._get_product_domain(),
    )

    def _base_product_domain(self):
        """
        Return a domain to be used when searching for products in the pricelist's item form.
        This domain ensures that only active products are returned.
        """
        return [
        '&',
        '|', ('product_tmpl_id', '=', None), ('product_tmpl_id.active', '=', True),
        '|', ('product_id', '=', None), ('product_id.active', '=', True)
        ]

    def _get_product_domain(self):
        """
        Return a domain for searching products in the pricelist's item form.
        This method utilizes the base product domain to ensure only active
        products are included in the search.
        """
        return self._base_product_domain()

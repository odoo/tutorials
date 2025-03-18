from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_best_pricing_rule(self, quantity=None, date=None, **kwargs):
        """Return the best pricing rule for the given duration.

        :return: least expensive pricing rule for given duration
        :rtype: product.pricelist.item
        """
        return self.product_tmpl_id._get_best_pricing_rule(quantity, date, product=self, **kwargs)

    def _compute_rental_default(self, duration, unit):
        """Return the default rental prices for the given duration.

        :return: default pricing for given duration
        :rtype: int
        """
        return self.product_tmpl_id._compute_rental_default(duration, unit)

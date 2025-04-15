from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    plan_id = fields.Many2one(comodel_name='sale.subscription.plan', string="Recurring Plan")

    def _compute_base_price(self, product, quantity, uom, date, currency, plan_id=None, **kwargs):
        """ override method to compute base price for subscription and rental products. """
        currency.ensure_one()

        if plan_id and product.recurring_invoice:
            rule_base = self.base or 'list_price'
            if rule_base == 'pricelist' and self.base_pricelist_id:
                price = self.base_pricelist_id._get_product_price(
                    product=product,
                    quantity=quantity,
                    uom=uom,
                    date=date,
                    plan_id=plan_id
                )

                src_currency = self.base_pricelist_id.currency_id
                if src_currency != currency:
                    price = src_currency._convert(price, currency, self.env.company, date, round=False)
                return price
        return super()._compute_base_price(product, quantity, uom, date, currency, **kwargs)

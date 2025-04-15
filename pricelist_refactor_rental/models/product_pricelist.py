from odoo import fields, models
from odoo.osv.expression import AND


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    product_rental_pricelist_ids = fields.One2many(
        comodel_name='product.pricelist.item',
        inverse_name='pricelist_id',
        string="Rental pricelist Rules",
        domain=lambda self: self._get_rental_product_domain(),
    )

    def _get_product_domain(self):
        return AND([
            super()._get_product_domain(),
            [('recurrence_id', '=', False)]
        ])

    def _get_rental_product_domain(self):
        return AND([
            self._base_product_domain(),
            [('recurrence_id', '!=', False)]
        ])

    def _compute_price_rule(
        self, products, quantity, currency=None, date=False, start_date=None, end_date=None, uom=None, **kwargs
    ):
        """ override method to compute price rule for rental. """

        self and self.ensure_one()  # self is at most one record
        currency = currency or self.currency_id or self.env.company.currency_id
        currency.ensure_one()

        if not products:
            return {}
        if not date:
            date = fields.Datetime.now()

        results = {}
        for product in products:
            if self._enable_rental_price(start_date, end_date) and product.rent_ok:
                pricelist_id = self.env['product.pricelist.item']
                if start_date and end_date:
                    pricelist_item_id = product._get_best_pricing_rule(
                        quantity=quantity,
                        date=date,
                        uom=uom,
                        start_date=start_date,
                        end_date=end_date,
                        pricelist=self,
                        currency=currency
                    )
                    duration_vals = pricelist_id._compute_duration_vals(start_date, end_date)
                    duration = pricelist_item_id and duration_vals[pricelist_item_id.recurrence_id.unit or 'day'] or 0
                else:
                    pricelist_item_id = pricelist_id._get_first_suitable_rental_pricelist_id(
                        product=product,
                        date=date,
                        pricelist=self
                    )
                    duration = pricelist_item_id.recurrence_id.duration

                if pricelist_item_id:
                    price = pricelist_item_id._compute_price_rental(
                        duration=duration,
                        unit=pricelist_item_id.recurrence_id.unit,
                        product=product,
                        quantity=quantity,
                        date=date,
                        start_date=start_date,
                        end_date=end_date,
                        uom=uom
                    )
                elif product.default_recurrence_id:
                    if start_date and end_date:
                        duration_vals = pricelist_id._compute_duration_vals(start_date, end_date)
                        duration = product.default_recurrence_id and duration_vals[product.default_recurrence_id.unit or 'day'] or 0
                    price = product._compute_rental_default(duration, product.default_recurrence_id)
                elif product._name == 'product.product':
                    price = product.lst_price
                else:
                    price = product.list_price
                results[product.id] = pricelist_item_id.currency_id._convert(
                    price, currency, self.env.company, date
                ), pricelist_item_id.id
        price_computed_products = self.env[products._name].browse(results.keys())

        return {
            **results,
            **super()._compute_price_rule(
                products - price_computed_products, quantity, currency=currency, date=date, **kwargs
            ),
        }

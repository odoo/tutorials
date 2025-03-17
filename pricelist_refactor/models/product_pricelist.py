from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    item_ids = fields.One2many(
        comodel_name='product.pricelist.item',
        inverse_name='pricelist_id',
        string="Pricing Rules",
        domain=[
            '&',
            '|', ('product_tmpl_id', '=', None), ('product_tmpl_id.active', '=', True),
            '|', ('product_id', '=', None), ('product_id.active', '=', True),
            ('plan_id', '=', None),
            ('recurrence_id', '=', None)
        ],
    )

    product_subscription_pricelist_ids = fields.One2many(
        comodel_name='product.pricelist.item',
        inverse_name='pricelist_id',
        string="Recurring Pricing Rules",
        domain=[
            '&',
            '|', ('product_tmpl_id', '=', None), ('product_tmpl_id.active', '=', True),
            '|', ('product_id', '=', None), ('product_id.active', '=', True),
            ('plan_id', '!=', None),
        ]
    )

    rental_pricelist_ids = fields.One2many(
        comodel_name='product.pricelist.item',
        inverse_name='pricelist_id',
        string="Rental Pricing Rules",
        domain=[
            '&',
            '|', ('product_tmpl_id', '=', None), ('product_tmpl_id.active', '=', True),
            '|', ('product_id', '=', None), ('product_id.active', '=', True),
            ('recurrence_id', '!=', None),
        ]
    )

    
    def _compute_price_rule(
        self, products, quantity, currency=None, date=False, start_date=None, end_date=None, plan_id=None, **kwargs
    ):
        """override method to compute price rule for rental and subscription."""
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
                Pricing = self.env['product.pricelist.item']
                if start_date and end_date:
                    pricing = product._get_best_pricing_rule(
                        quantity, date, uom=kwargs.get("uom"), start_date=start_date, end_date=end_date, pricelist=self, currency=currency
                    )
                    duration_vals = Pricing._compute_duration_vals(start_date, end_date)
                    duration = pricing and duration_vals[pricing.recurrence_id.unit or 'day'] or 0
                else:
                    pricing = Pricing._get_first_suitable_pricing(product, self)
                    duration = pricing.recurrence_id.duration
                if pricing:
                    price = pricing._compute_price_rental(duration, pricing.recurrence_id.unit, product, quantity, date, start_date, end_date, uom=kwargs.get("uom"))
                elif product.default_rent_unit:
                    duration_vals = Pricing._compute_duration_vals(start_date, end_date)
                    duration = product.default_rent_unit and duration_vals[pricing.recurrence_id.unit or 'day'] or 0
                    price = product._compute_rental_default(duration, product.default_rent_unit)
                elif product._name == 'product.product':
                    price = product.lst_price
                else:
                    price = product.list_price
                results[product.id] = pricing.currency_id._convert(
                    price, currency, self.env.company, date
                ), False
            elif product.recurring_invoice:
                results[product.id] = self.env['product.pricelist.item']._get_first_suitable_recurring_pricing(product, plan=plan_id, pricelist=self)._compute_price(product, quantity, kwargs.get('uom'), date, plan_id=plan_id), self.env['product.pricelist.item']._get_first_suitable_recurring_pricing(product, plan=plan_id, pricelist=self).id
        price_computed_products = self.env[products._name].browse(results.keys())
        return {
            **results,
            **super()._compute_price_rule(
                products - price_computed_products, quantity, currency=currency, date=date, **kwargs
            ),
        }

    def _enable_rental_price(self, start_date, end_date):
        """Determine if rental pricing should be used."""
        return bool(start_date and end_date)

from odoo import api, fields, models, tools
import math
from dateutil.relativedelta import relativedelta

PERIOD_RATIO = {
    'hour': 1,
    'day': 24,
    'week': 24 * 7,
    'month': 24 * 31,
    'year': 24 * 31 * 12,
}


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    active = fields.Boolean("Active", default=True)
    plan_id = fields.Many2one('sale.subscription.plan', string="Recurring Plan")
    recurrence_id = fields.Many2one('sale.temporal.recurrence', string="Renting Period")

    @api.model
    def _get_first_suitable_recurring_pricing(self, product, plan=None, pricelist=None):
        """ Get a suitable pricing for given product and pricelist."""
        product_sudo = product.sudo()
        is_product_template = product_sudo._name == "product.template"
        available_pricings = product_sudo.subscription_pricelist_rule_ids
        first_pricing = self.env['product.pricelist.item']
        for pricing in available_pricings:
            if plan and pricing.plan_id != plan:
                continue
            if pricing.pricelist_id == pricelist and (is_product_template or pricing._applies_to(product_sudo)):
                return pricing
            if not first_pricing and pricing.pricelist_id and (is_product_template or pricing._applies_to(product_sudo)):
                # If price list and current pricing is not part of it,
                # We store the first one to return if not pricing matching the price list is found.
                first_pricing = pricing
        return first_pricing

    @api.model
    def _get_first_suitable_rental_pricing(self, product, recurrence_id=None, pricelist=None):
        """ Get a suitable pricing for given product and pricelist."""
        product_sudo = product.sudo()
        is_product_template = product_sudo._name == "product.template"
        available_pricings = product_sudo.rental_pricelist_rule_ids
        first_pricing = self.env['product.pricelist.item']
        for pricing in available_pricings:
            if recurrence_id and pricing.recurrence_id != recurrence_id:
                continue
            if pricing.pricelist_id == pricelist and (is_product_template or pricing._applies_to(product_sudo)):
                return pricing
            if not first_pricing and pricing.pricelist_id and (is_product_template or pricing._applies_to(product_sudo)):
                # If price list and current pricing is not part of it,
                # We store the first one to return if not pricing matching the price list is found.
                first_pricing = pricing
        return first_pricing

    def _compute_price_rental(self, duration, unit, product, quantity, date, start_date, end_date, **kwargs):
        """Compute price based on the duration and unit."""
        self.ensure_one()
        if duration <= 0 or self.recurrence_id.duration <= 0:
            return self._compute_price(product, quantity, kwargs.get("uom"), date, start_date=start_date, end_date=end_date)
        if unit != self.recurrence_id.unit:
            converted_duration = math.ceil(
                (duration * PERIOD_RATIO[unit]) / (self.recurrence_id.duration * PERIOD_RATIO[self.recurrence_id.unit])
            )
        else:
            converted_duration = math.ceil(duration / self.recurrence_id.duration)
        return self._compute_price(product, quantity, kwargs.get("uom"), date, start_date=start_date, end_date=end_date) * converted_duration

    @api.model
    def _compute_duration_vals(self, start_date, end_date):
        """Compute duration in various temporal units."""
        duration = end_date - start_date
        vals = {
            'hour': (duration.days * 24 + duration.seconds / 3600),
            'day': math.ceil((duration.days * 24 + duration.seconds / 3600) / 24),
            'week': math.ceil((duration.days * 24 + duration.seconds / 3600) / (24 * 7)),
        }
        duration_diff = relativedelta(end_date, start_date)
        months = 1 if any([duration_diff.days, duration_diff.hours, duration_diff.minutes]) else 0
        months += duration_diff.months + duration_diff.years * 12
        vals['month'] = months
        vals['year'] = months / 12
        return vals

    @api.model
    def _get_suitable_pricings(self, product, pricelist=None, first=False):
        """Get the suitable pricings for a product."""
        is_product_template = product._name == "product.template"
        available_pricings = self.env['product.pricelist.item']
        if pricelist:
            for pricing in product.rental_pricelist_rule_ids:
                if pricing.pricelist_id == pricelist\
                    and (is_product_template or pricing._applies_to(product)):
                    if first:
                        return pricing
                    available_pricings |= pricing

        for pricing in product.rental_pricelist_rule_ids:
            if not pricing.pricelist_id and (is_product_template or pricing._applies_to(product)):
                if first:
                    return pricing
                available_pricings |= pricing

        return available_pricings

    def _applies_to(self, product):
        """ Check whether current pricing applies to given product.
        :param product.product product:
        :return: true if current pricing is applicable for given product, else otherwise.
        :rtype: bool
        """
        self.ensure_one()
        return (
            self.product_tmpl_id == product.product_tmpl_id
            and (
                self.applied_on == "1_product"
                or product == self.product_id))

    def _compute_price(self, product, quantity, uom, date, currency=None, plan_id=None, start_date=None, end_date=None, *kwargs):
        """Compute the unit price of a product in the context of a pricelist application.

        Note: self and self.ensure_one()

        :param product: recordset of product (product.product/product.template)
        :param float qty: quantity of products requested (in given uom)
        :param uom: unit of measure (uom.uom record)
        :param datetime date: date to use for price computation and currency conversions
        :param currency: currency (for the case where self is empty)

        :returns: price according to pricelist rule or the product price, expressed in the param
                    currency, the pricelist currency or the company currency
        :rtype: float
        """
        self and self.ensure_one()  # self is at most one record
        product.ensure_one()
        uom.ensure_one()

        currency = currency or self.currency_id or self.env.company.currency_id
        currency.ensure_one()

        # Pricelist specific values are specified according to product UoM
        # and must be multiplied according to the factor between uoms
        product_uom = product.uom_id
        if product_uom != uom:
            convert = lambda p: product_uom._compute_price(p, uom)
        else:
            convert = lambda p: p
        if self.compute_price == 'fixed':
            price = convert(self.fixed_price)
        elif self.compute_price == 'percentage':
            if plan_id:
                base_price = self._compute_base_price(product, quantity, uom, date, currency, plan_id=plan_id)
            elif start_date and end_date:
                base_price = self._compute_base_price(product, quantity, uom, date, currency, recurrence_id=self.recurrence_id)
            else:
                base_price = self._compute_base_price(product, quantity, uom, date, currency)
            price = (base_price - (base_price * (self.percent_price / 100))) or 0.0
        elif self.compute_price == 'formula':
            if plan_id:
                base_price = self._compute_base_price(product, quantity, uom, date, currency, plan_id=plan_id)
            elif start_date and end_date:
                base_price = self._compute_base_price(product, quantity, uom, date, currency, recurrence_id=self.recurrence_id)
            else:
                base_price = self._compute_base_price(product, quantity, uom, date, currency)
                
            # complete formula
            price_limit = base_price
            price = (base_price - (base_price * (self.price_discount / 100))) or 0.0
            if self.price_round:
                price = tools.float_round(price, precision_rounding=self.price_round)

            if self.price_surcharge:
                price += convert(self.price_surcharge)

            if self.price_min_margin:
                price = max(price, price_limit + convert(self.price_min_margin))

            if self.price_max_margin:
                price = min(price, price_limit + convert(self.price_max_margin))
        else:  # empty self, or extended pricelist price computation logic
            price = self._compute_base_price(product, quantity, uom, date, currency)

        return price

    def _compute_base_price(self, product, quantity, uom, date, currency, plan_id=None, recurrence_id=None):
        """override method to compute base price for subscription and rental products."""
        currency.ensure_one()
        if plan_id and product.recurring_invoice:
            rule_base = self.base or 'list_price'
            if rule_base == 'pricelist' and self.base_pricelist_id:
                price = self._get_first_suitable_recurring_pricing(product, plan_id, self.base_pricelist_id)._compute_price(product, quantity, uom, date)
                src_currency = self.base_pricelist_id.currency_id
                if src_currency != currency:
                    price = src_currency._convert(price, currency, self.env.company, date, round=False)
                return price
        elif recurrence_id and product.rent_ok:
            rule_base = self.base or 'list_price'
            if rule_base == 'pricelist' and self.base_pricelist_id:
                breakpoint()
                price = self._get_first_suitable_rental_pricing(product, recurrence_id, self.base_pricelist_id)._compute_price(product, quantity, uom, date)
                src_currency = self.base_pricelist_id.currency_id
                if src_currency != currency:
                    price = src_currency._convert(price, currency, self.env.company, date, round=False)
                return price
        return super()._compute_base_price(product, quantity, uom, date, currency)

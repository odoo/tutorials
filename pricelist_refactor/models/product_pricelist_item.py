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

    active = fields.Boolean(string="Active", default=True)
    plan_id = fields.Many2one(comodel_name='sale.subscription.plan', string="Recurring Plan")
    recurrence_id = fields.Many2one(comodel_name='sale.temporal.recurrence', string="Renting Period")

    @api.model
    def _get_first_suitable_rental_pricelist_id(self, product, date, start_date, end_date, recurrence_id=None, pricelist=None):
        """ Get a suitable pricing for given product and pricelist."""
        product_sudo = product.sudo()
        is_product_template = product_sudo._name == "product.template"
        available_product_pricelist_item_ids = product_sudo.rental_pricelist_rule_ids
        first_pricelist_item_id = self.env['product.pricelist.item']
        for product_pricelist_item_id in available_product_pricelist_item_ids:
            if not start_date or not end_date:
                continue
            duration_vals = self._compute_duration_vals(start_date, end_date)[product_pricelist_item_id.recurrence_id.unit]
            if recurrence_id and product_pricelist_item_id.recurrence_id != recurrence_id:
                continue
            if product_pricelist_item_id._is_applies_to_rental(product, pricelist, is_product_template, duration_vals, date):
                return product_pricelist_item_id

        # if no pricelist item is found for the product, search for a pricelist item based on the product category.
        pricelist_item_ids = self.env['product.pricelist.item']._read_group(
            domain=[
                ('pricelist_id', '=', pricelist.id),
                ('recurrence_id', '!=', False),
                '|', ('categ_id', 'parent_of', product.categ_id.ids),
                '&', ('product_tmpl_id', '=', False), ('product_id', '=', False),
                '|', ('date_start', '=', False), ('date_start', '<=', date),
                '|', ('date_end', '=', False), ('date_end', '>=', date)
            ],
            groupby=['categ_id'],
            aggregates=['id:recordset'],
            limit=1
        )
        if pricelist_item_ids:
            for pricelist_item_id in pricelist_item_ids[0][1]:
                if recurrence_id and pricelist_item_id.recurrence_id == recurrence_id and pricelist_item_id.min_quantity <= duration_vals:
                    return pricelist_item_id
        return first_pricelist_item_id

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
    def _get_suitable_pricelist_ids(self, product, pricelist, start_date, end_date, date):
        """Get the suitable pricings for a product."""
        is_product_template = product._name == "product.template"
        available_pricelist_ids = self.env['product.pricelist.item']
        if pricelist:
            for price_rule_id in product.rental_pricelist_rule_ids:
                duration_vals = self._compute_duration_vals(start_date, end_date)[price_rule_id.recurrence_id.unit]
                if price_rule_id.pricelist_id == pricelist \
                    and (is_product_template or price_rule_id._is_applies_to_rental(product, pricelist, is_product_template, duration_vals, date)):
                    available_pricelist_ids |= price_rule_id
        if not available_pricelist_ids:
            self and self.ensure_one()  # self is at most one record
            pricelist_item_ids = self.env['product.pricelist.item']._read_group(
                domain=[
                    ('pricelist_id', '=', pricelist.id),
                    ('recurrence_id', '!=', False),
                    '|', ('categ_id', 'parent_of', product.categ_id.ids),
                    '&', ('product_tmpl_id', '=', False), ('product_id', '=', False),
                    '|', ('date_start', '=', False), ('date_start', '<=', date),
                    '|', ('date_end', '=', False), ('date_end', '>=', date)
                ],
                groupby=['categ_id'],
                aggregates=['id:recordset'],
                limit=1
            )
            if pricelist_item_ids:
                for pricelist_id in pricelist_item_ids[0][1]:
                    duration_vals = self._compute_duration_vals(start_date, end_date)[pricelist_id.recurrence_id.unit]
                    if pricelist_id.min_quantity <= duration_vals:
                        available_pricelist_ids |= pricelist_id
                    else:
                        break
        return available_pricelist_ids

    def _compute_price_rental(self, duration, unit, product, quantity, date, start_date, end_date, uom=None, **kwargs):
        """Compute price based on the duration and unit."""
        self.ensure_one()
        if duration <= 0 or self.recurrence_id.duration <= 0:
            return self._compute_price(product, quantity, uom, date, start_date=start_date, end_date=end_date)
        if unit != self.recurrence_id.unit:
            converted_duration = math.ceil(
                (duration * PERIOD_RATIO[unit]) / (self.recurrence_id.duration * PERIOD_RATIO[self.recurrence_id.unit])
            )
        else:
            converted_duration = math.ceil(duration / self.recurrence_id.duration)
        return self._compute_price(product, quantity, uom, date, start_date=start_date, end_date=end_date, converted_duration=converted_duration)

    def _is_applies_to_rental(self, product, pricelist, is_product_template, duration_vals, date):
        """ Check whether current pricing applies to given product.
        :param product.product product:
        :return: true if current pricing is applicable for given product, else otherwise.
        :rtype: bool
        """
        return (
            self.pricelist_id == pricelist
            and (
                is_product_template 
                or self.product_tmpl_id == product.product_tmpl_id
                and (
                    self.applied_on == "1_product"
                    or product == self.product_id
                )
            )
            and self.min_quantity <= duration_vals
            and (
                not self.date_start
                or self.date_start <= date
            )
            and (
                not self.date_end
                or self.date_end >= date
            )
        )

    def _compute_price(self, product, quantity, uom, date, currency=None, plan_id=None, converted_duration=None, start_date=None, end_date=None, *kwargs):
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
            if converted_duration:
                price = convert(self.fixed_price * converted_duration)
            else:
                price = convert(self.fixed_price)
        elif self.compute_price == 'percentage':
            if plan_id:
                base_price = self._compute_base_price(product, quantity, uom, date, currency, plan_id=plan_id)
            elif converted_duration:
                base_price = self._compute_base_price(product, quantity, uom, date, currency, recurrence_id=self.recurrence_id, start_date=start_date, end_date=end_date, converted_duration=converted_duration)
            else:
                base_price = self._compute_base_price(product, quantity, uom, date, currency)
            price = (base_price - (base_price * (self.percent_price / 100))) or 0.0
        elif self.compute_price == 'formula':
            if plan_id:
                base_price = self._compute_base_price(product, quantity, uom, date, currency, plan_id=plan_id)
            elif converted_duration:
                base_price = self._compute_base_price(product, quantity, uom, date, currency, recurrence_id=self.recurrence_id, start_date=start_date, end_date=end_date, converted_duration=converted_duration)
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

    def _compute_base_price(self, product, quantity, uom, date, currency, plan_id=None, recurrence_id=None, converted_duration=None, start_date=None, end_date=None):
        """override method to compute base price for subscription and rental products."""
        currency.ensure_one()
        if plan_id and product.recurring_invoice:
            rule_base = self.base or 'list_price'
            if rule_base == 'pricelist' and self.base_pricelist_id:
                price = self.base_pricelist_id._get_product_price(product, quantity, uom, date, plan_id=plan_id)
                src_currency = self.base_pricelist_id.currency_id
                if src_currency != currency:
                    price = src_currency._convert(price, currency, self.env.company, date, round=False)
                return price
        elif recurrence_id and product.rent_ok:
            duration_vals = self._compute_duration_vals(start_date, end_date)
            converted_duration = self and duration_vals[self.recurrence_id.unit or 'day'] or 0
            rule_base = self.base or 'list_price'
            if rule_base == 'pricelist' and self.base_pricelist_id:
                price = self._get_first_suitable_rental_pricelist_id(
                    product, date, start_date, end_date, recurrence_id, self.base_pricelist_id
                )._compute_price(product, quantity, uom, date)
                src_currency = self.base_pricelist_id.currency_id
                if src_currency != currency:
                    price = src_currency._convert(price, currency, self.env.company, date, round=False)
                if converted_duration:
                    return price*converted_duration
                return price
        return super()._compute_base_price(product, quantity, uom, date, currency)

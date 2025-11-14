from math import ceil

from odoo import models
from odoo.http import request
from odoo.tools import format_amount

from odoo.addons.sale_renting.models.product_pricing import PERIOD_RATIO


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_additionnal_combination_info(self, product_or_template, quantity, date, website):
        """ Override to add the information about renting for rental products

        If the product is rent_ok, this override adds the following information about the rental:
            - is_rental: Whether combination is rental,
            - rental_duration: The duration of the first defined product pricing on this product
            - rental_unit: The unit of the first defined product pricing on this product
            - default_start_date: If no pickup nor rental date in context, the start_date of the
                                   first renting sale order line in the cart;
            - default_end_date: If no pickup nor rental date in context, the end_date of the
                                   first renting sale order line in the cart;
            - current_rental_duration: If no pickup nor rental date in context, see rental_duration,
                                       otherwise, the duration between pickup and rental date in the
                                       current_rental_unit unit.
            - current_rental_unit: If no pickup nor rental date in context, see rental_unit,
                                   otherwise the unit of the best pricing for the renting between
                                   pickup and rental date.
            - current_rental_price: If no pickup nor rental date in context, see price,
                                    otherwise the price of the best pricing for the renting between
                                    pickup and rental date.
        """
        res = super()._get_additionnal_combination_info(product_or_template, quantity, date, website)
        if not product_or_template.rent_ok:
            return res

        res['list_price'] = res['price']
        currency = website.currency_id
        pricelist = website.pricelist_id
        ProductPricing = self.env['product.pricelist.item']
        default_recurrence_id = product_or_template.default_recurrence_id

        pricelist_id = ProductPricing._get_first_suitable_rental_pricelist_id(product_or_template, date, pricelist=pricelist)
        if not pricelist_id and not default_recurrence_id:
            return res

        order = website.sale_get_order() if website and request else self.env['sale.order']
        start_date = self.env.context.get('start_date') or order.rental_start_date
        end_date = self.env.context.get('end_date') or order.rental_return_date
        if start_date and end_date:
            current_pricing = product_or_template._get_best_pricing_rule(
                start_date=start_date,
                end_date=end_date,
                pricelist=pricelist,
                currency=currency,
            )
            current_recurrence_id = current_pricing.recurrence_id if current_pricing else default_recurrence_id
            current_unit = current_recurrence_id.unit
            current_duration = ProductPricing._compute_duration_vals(start_date, end_date)[current_unit]
        else:
            current_recurrence_id = pricelist_id.recurrence_id if pricelist_id else default_recurrence_id
            current_unit = current_recurrence_id.unit
            current_duration = current_recurrence_id.duration
            current_pricing = pricelist_id

        current_price = pricelist._get_product_price(
            product=product_or_template,
            quantity=quantity,
            currency=currency,
            start_date=start_date,
            end_date=end_date,
        )

        default_start_date, default_end_date = self._get_default_renting_dates(
            start_date, end_date, current_duration, current_unit
        )

        ratio = ceil(current_duration) / pricelist_id.recurrence_id.duration if pricelist_id.recurrence_id.duration else 1
        if current_unit != pricelist_id.recurrence_id.unit and not default_recurrence_id:
            ratio *= PERIOD_RATIO[current_unit] / PERIOD_RATIO[pricelist_id.recurrence_id.unit]

        # apply taxes
        product_taxes = res['product_taxes']
        if product_taxes:
            current_price = self.env['product.template']._apply_taxes_to_price(
                current_price, currency, product_taxes, res['taxes'], product_or_template,
            )

        suitable_pricelist_ids = ProductPricing._get_suitable_pricelist_ids(product_or_template, pricelist, date)
        # If there are multiple pricings with the same recurrence, we only keep the cheapest ones
        best_pricings = {}
        for pricelist_id in suitable_pricelist_ids:
            recurrence_id = pricelist_id.recurrence_id
            current = best_pricings.get(recurrence_id)

            if not current or current._compute_price(
                self, quantity, product_or_template.uom_id, date, currency=currency
            ) > pricelist_id._compute_price(
                self, quantity, product_or_template.uom_id, date, currency=currency
            ):
                best_pricings[recurrence_id] = pricelist_id

        suitable_pricelist_ids = best_pricings.values()

        def _pricing_price(pricelist_id):
            price = pricelist_id._compute_price(self, quantity, product_or_template.uom_id, date, currency=currency)
            if product_taxes:
                price = self.env['product.template']._apply_taxes_to_price(
                    price, currency, product_taxes, res['taxes'], product_or_template
                )
            else:
                price = pricelist_id.price
            if pricelist_id.currency_id == currency:
                return price
            return pricelist_id.currency_id._convert(
                from_amount=price,
                to_currency=currency,
                company=self.env.company,
                date=date,
            )
        pricing_table = [
            (pricelist_id.recurrence_id.duration_display, format_amount(self.env, _pricing_price(pricelist_id), currency))
            for pricelist_id in suitable_pricelist_ids
        ]
        recurrence = pricelist_id.recurrence_id if pricelist_id else default_recurrence_id

        return {
            **res,
            'is_rental': True,
            'rental_duration': recurrence.duration,
            'rental_duration_unit': recurrence.unit,
            'rental_unit': recurrence._get_unit_label(recurrence.duration),
            'default_start_date': default_start_date,
            'default_end_date': default_end_date,
            'current_rental_duration': ceil(current_duration),
            'current_rental_unit': current_recurrence_id._get_unit_label(current_duration),
            'current_rental_price': current_price,
            'current_rental_price_per_unit': current_price / (ratio or 1),
            'base_unit_price': 0,
            'base_unit_name': False,
            'pricing_table': pricing_table,
            'prevent_zero_price_sale': website.prevent_zero_price_sale and currency.is_zero(
                current_price,
            ),
        }

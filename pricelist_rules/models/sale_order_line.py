# Part of Odoo. See LICENSE file for full copyright and licensing details.

import math
from datetime import datetime

from odoo import api, fields, models

PERIOD_CONVERSION = {
    'hour': 1,
    'day': 24,
    'week': 24 * 7,
    'month': 24 * 31,
    'year': 24 * 31 * 12,
}

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('start_date', 'return_date', 'product_id', 'product_uom_qty')
    def _compute_price_unit(self):
        productPricing = self.env['product.pricing']

        for line in self:
            order = line.order_id
            product = line.product_id
            
            if product.recurring_invoice:
                line._compute_price_unit_subscription()
                continue

            if not order or not line.start_date or not line.return_date or not product:
                continue

            pricing = product.product_tmpl_id[:1]._get_best_pricing_rule(
                start_date=line.start_date,
                end_date=line.return_date,
                pricelist=order.pricelist_id,
                currency=order.currency_id
            )

            if not pricing or pricing.recurrence_id.duration <= 0:
                continue

            computed_duration_values = productPricing._compute_duration_vals(line.start_date, line.return_date)
            billing_unit = pricing.recurrence_id.unit
            rental_duration = computed_duration_values.get(billing_unit, 0)

            converted_duration = (
                math.ceil(rental_duration / pricing.recurrence_id.duration)
                if billing_unit == pricing.recurrence_id.unit
                else math.ceil((rental_duration * PERIOD_CONVERSION[billing_unit]) / 
                               (pricing.recurrence_id.duration * PERIOD_CONVERSION[pricing.recurrence_id.unit]))
            )
            if pricing.min_quantity <= converted_duration:
                rental_price = pricing._compute_price_rental(
                    product=product,
                    quantity=converted_duration,
                    uom=line.product_uom,
                    date=order.date_order,
                    currency=line.currency_id,
                )
                line.price_unit = rental_price * converted_duration
            else:
                line.price_unit = pricing.price * converted_duration

        super()._compute_price_unit()

    @api.depends('product_id', 'product_uom', 'product_uom_qty', 'order_id.end_date', 'order_id.date_order')
    def _compute_price_unit_subscription(self):
        all_prices_skipped = True  

        for line in self:
            if not line._is_valid_order():
                continue

            pricelist_item = line._get_pricelist_item()
            if pricelist_item:
                start_date = fields.Date.to_date(line.order_id.date_order)
                end_date = fields.Date.to_date(line.order_id.end_date)

                duration_vals = self.env['product.pricing']._compute_duration_vals(start_date, end_date)
                duration = duration_vals.get(pricelist_item.plan_id.billing_period_unit, 0)

                if duration >= pricelist_item.min_quantity:
                    line.price_unit = pricelist_item._compute_price(
                        product=line.product_id,
                        quantity=duration,
                        uom=line.product_uom,
                        date=line.order_id.date_order,
                        currency=line.currency_id,
                    )
                    all_prices_skipped = False

        if all_prices_skipped:
            super()._compute_price_unit()
    def _is_valid_order(self):
        order = self.order_id
        return bool(order and self.product_id and order.plan_id and order.pricelist_id and order.date_order and order.end_date)

    def _get_pricelist_item(self):
        return self.env['sale.subscription.pricing'].search([
            ('product_template_id', '=', self.product_id.product_tmpl_id.id),
            ('pricelist_id', '=', self.order_id.pricelist_id.id),
            ('plan_id', '=', self.order_id.plan_id.id)
        ], limit=1)

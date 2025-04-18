from odoo import models
from odoo.http import request
from odoo.tools import format_amount


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_pricelist_item_ids(self, pricelist, date, product=None):
        self.ensure_one()
        is_template = not product and self._name == 'product.template'
        res = self.env['sale.subscription.plan']
        quantity = self.env.context.get('quantity', 1.0)
        for pricelist_id in pricelist._get_applicable_rules(self, date, plan_id='all'):
            if not is_template and not pricelist_id._is_applicable_for(product or self, quantity):
                continue
            if pricelist_id.plan_id not in res:
                yield pricelist_id
                res |= pricelist_id.plan_id

    def _get_additionnal_combination_info(self, product_or_template, quantity, date, website):
        res = super()._get_additionnal_combination_info(product_or_template, quantity, date, website)
        if not product_or_template.recurring_invoice:
            return res

        res['list_price'] = res['price']
        currency = website.currency_id
        pricelist = website.pricelist_id
        requested_plan = request and request.params.get('plan_id')
        requested_plan = requested_plan and requested_plan.isdigit() and int(requested_plan)
        possible_pricing_count = 0
        pricings = []
        default_pricing = False

        for pricelist_id in product_or_template.sudo()._get_pricelist_item_ids(pricelist, date):
            price = pricelist_id._compute_price(self, quantity, product_or_template.uom_id, date,
                                                currency=currency, plan_id=pricelist_id.plan_id.id)
            if pricelist_id.currency_id != currency:
                price = pricelist_id.currency_id._convert(
                    from_amount=price,
                    to_currency=currency,
                    company=self.env.company,
                    date=date,
                )

            if res.get('product_taxes', False):
                price = self.env['product.template']._apply_taxes_to_price(
                    price, currency, res['product_taxes'], res['taxes'], product_or_template,
                )

            price_format = format_amount(self.env, amount=price, currency=currency)
            pricelist_id = {
                'plan_id': pricelist_id.plan_id.id,
                'price': f"{pricelist_id.plan_id.name}: {price_format}",
                'price_value': price,
                'table_price': price_format,
                'table_name': pricelist_id.plan_id.name.replace(' ', ' '),
                'can_be_added': product_or_template._website_can_be_added(pricelist=pricelist, pricelist_id=pricelist_id)
            }
            possible_pricing_count += 1 if pricelist_id['can_be_added'] else 0

            if (not default_pricing or pricelist_id['plan_id'] == requested_plan) and pricelist_id['can_be_added']:
                default_pricing = pricelist_id
            pricings += [pricelist_id]

        if pricings:
            plan_ids = self.env['sale.subscription.plan'].browse(pricelist_id['plan_id'] for pricelist_id in pricings)
            to_year = {'year': 1, 'month': 12, 'week': 52}
            translation_mapping = {'year': 'year', 'month': 'month', 'week': 'week'}
            minimum_period = min(plan_ids.mapped('billing_period_unit'), key=lambda x: 1 / to_year[x])

            for pricelist_id in pricings:
                plan_id = plan_ids.browse(pricelist_id['plan_id'])
                price = (
                    pricelist_id['price_value'] /
                    plan_id.billing_period_value *
                    to_year[plan_id.billing_period_unit] /
                    to_year[minimum_period]
                )
                pricelist_id['to_minimum_billing_period'] = f'{format_amount(self.env, amount=price, currency=currency)} / {translation_mapping.get(minimum_period, minimum_period)}'

        if not pricings:
            res.update({
                'is_subscription': True,
                'is_plan_possible': False,
                'pricings': False,
            })
            return res

        unit_price = default_pricing['price_value'] if default_pricing else 0
        return {
            **res,
            'is_subscription': True,
            'pricings': pricings,
            'is_plan_possible': possible_pricing_count > 0,
            'price': unit_price,
            'subscription_default_pricing_price': default_pricing['price'] if default_pricing else '',
            'subscription_default_pricing_plan_id': default_pricing['plan_id'] if default_pricing else False,
            'subscription_pricing_select': possible_pricing_count > 1,
            'prevent_zero_price_sale': website.prevent_zero_price_sale and currency.is_zero(
                unit_price,
            ),
        }

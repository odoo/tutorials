import math
from odoo import fields, models

PERIOD_RATIO = {
    'hour': 1,
    'day': 24,
    'week': 24 * 7,
    'month': 24 * 31,
    'year': 24 * 31 * 12,
}


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pricelist_rule_ids = fields.One2many(
        string="Pricelist Rules",
        comodel_name='product.pricelist.item',
        inverse_name='product_tmpl_id',
        domain=lambda self: [
            '|',
            ('product_tmpl_id', 'in', self.ids),
            ('product_id', 'in', self.product_variant_ids.ids),
            ('plan_id', '=', None),
            ('recurrence_id', '=', None)
        ]
    )
    subscription_pricelist_rule_ids = fields.One2many(
        string="Subscription Pricelist Rules",
        comodel_name='product.pricelist.item',
        inverse_name='product_tmpl_id',
        domain=lambda self: [
            '|',
            ('product_tmpl_id', 'in', self.ids),
            ('product_id', 'in', self.product_variant_ids.ids),
            ('plan_id', '!=', False)
        ]
    )
    rental_pricelist_rule_ids = fields.One2many(
        string="Rental Pricelist Rules",
        comodel_name='product.pricelist.item',
        inverse_name='product_tmpl_id',
        domain=lambda self: [
            '|',
            ('product_tmpl_id', 'in', self.ids),
            ('product_id', 'in', self.product_variant_ids.ids),
            ('recurrence_id', '!=', False)
        ]
    )
    
    default_rent_unit = fields.Many2one(comodel_name='sale.temporal.recurrence', string="Default Sale Unit")

    def _get_best_pricing_rule(self, quantity, date, product=False, start_date=False, end_date=False, **kwargs):
        """ Return the best pricing rule for the given duration.

        :param ProductProduct product: a product recordset (containing at most one record)
        :param datetime start_date: start date of leasing period
        :param datetime end_date: end date of leasing period
        :return: least expensive pricing rule for given duration
        """
        self.ensure_one()
        best_pricing_rule = self.env['product.pricelist.item']
        if not self.product_pricing_ids or not (start_date and end_date):
            return best_pricing_rule
        pricelist = kwargs.get('pricelist', self.env['product.pricelist'])
        currency = kwargs.get('currency', self.currency_id)
        company = kwargs.get('company', self.env.company)
        duration_dict = self.env['product.pricelist.item']._compute_duration_vals(start_date, end_date)
        min_price = float("inf")  # positive infinity
        available_pricings = self.env['product.pricelist.item']._get_suitable_pricings(
            product or self, pricelist=pricelist
        )
        for pricing in available_pricings:
            unit = pricing.recurrence_id.unit
            price = pricing._compute_price_rental(duration_dict[unit], unit, product, quantity, date, start_date, end_date, uom=kwargs.get("uom"),base_price=kwargs.get("base_price"))
            if pricing.currency_id != currency:
                price = pricing.currency_id._convert(
                    from_amount=price,
                    to_currency=currency,
                    company=company,
                    date=fields.Date.today(),
                )
            if price < min_price:
                min_price, best_pricing_rule = price, pricing
        return best_pricing_rule

    def _compute_rental_default(self, duration, unit):
        """computing default rental price when no rule is avilable for rental product"""
        if duration <= 0:
            return self.list_price
        converted_duration = math.ceil(duration / self.default_rent_unit.duration)
        return self.list_price * converted_duration

import math
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.tools import format_amount

from odoo.addons.sale_renting.models.product_pricing import PERIOD_RATIO


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    recurrence_id = fields.Many2one(comodel_name='sale.temporal.recurrence', string="Renting Period")
    description = fields.Char(compute='_compute_description')

    def _compute_description(self):
        """ Compute description of a rental pricelist item.

        :return: string in the form 'price / duration'
        :rtype: str
        """
        for pricelist_id in self:
            pricelist_id.description = _(
                "%(amount)s / %(duration)s",
                amount=format_amount(self.env, amount=pricelist_id.fixed_price, currency=pricelist_id.currency_id),
                duration=pricelist_id.recurrence_id.duration_display
            )

    @api.model
    def _get_first_suitable_rental_pricelist_id(self, product, date, pricelist=None, **kwargs):
        """ Get the first suitable rental pricelist item for a given product and conditions. """
        return self._get_suitable_pricelist_ids(product, pricelist, date, first_match=True, **kwargs)

    @api.model
    def _get_suitable_pricelist_ids(self, product, pricelist, date, start_date=None, end_date=None, recurrence_id=None, first_match=False):
        """ Get all suitable pricelist items for a given product and conditions. """

        duration_vals = self._compute_duration_vals(start_date, end_date) if start_date and end_date else None
        available_pricelist_items = self.env['product.pricelist.item']
        default_pricelist = self.env['product.pricelist'].search([], limit=1)
        applicable_pricelists = [pricelist.id, default_pricelist.id] if pricelist else [default_pricelist.id]

        # Search for product-specific pricelist items
        for price_rule in reversed(product.rental_pricelist_rule_ids):
            if recurrence_id and price_rule.recurrence_id != recurrence_id:
                continue
            if (
                price_rule.pricelist_id.id in applicable_pricelists and
                price_rule._is_applicable_for(product, duration_vals[price_rule.recurrence_id.unit]
                if duration_vals else 1.0, date, applicable_pricelists)
            ):
                if first_match:
                    return price_rule
                available_pricelist_items |= price_rule

        # If no product-specific rules found, search based on category
        if not available_pricelist_items:
            pricelist_item_ids = self.env['product.pricelist.item']._read_group(
                domain=[
                    ('pricelist_id', 'in', applicable_pricelists),
                    ('recurrence_id', '!=', False),
                    '&', ('categ_id', 'parent_of', product.categ_id.ids),
                    '&', ('product_tmpl_id', '=', False), ('product_id', '=', False),
                    '|', ('date_start', '=', False), ('date_start', '<=', date),
                    '|', ('date_end', '=', False), ('date_end', '>=', date)
                ],
                groupby=['categ_id'],
                aggregates=['id:recordset'],
                limit=1
            )
            for pricelist_item in reversed(pricelist_item_ids[0][1]) if pricelist_item_ids else []:
                if duration_vals and pricelist_item.min_quantity <= duration_vals[pricelist_item.recurrence_id.unit]:
                    if first_match:
                        return pricelist_item
                    available_pricelist_items |= pricelist_item
        return available_pricelist_items

    @api.model
    def _compute_duration_vals(self, start_date, end_date):
        """ Compute duration in various temporal units. """
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

    def _compute_price_rental(self, duration, unit, product, quantity, date, start_date, end_date, uom=None, **kwargs):
        """ Compute price based on the duration and unit. """
        self.ensure_one()

        if duration <= 0 or self.recurrence_id.duration <= 0:
            return self._compute_price(
                product=product,
                quantity=quantity,
                uom=uom,
                date=date,
                start_date=start_date,
                end_date=end_date
            )
        if unit != self.recurrence_id.unit:
            converted_duration = math.ceil(
                (duration * PERIOD_RATIO[unit]) / (self.recurrence_id.duration * PERIOD_RATIO[self.recurrence_id.unit])
            )
        else:
            converted_duration = math.ceil(duration / self.recurrence_id.duration)

        return self._compute_price(
            product=product,
            quantity=quantity,
            uom=uom,
            date=date,
            start_date=start_date,
            end_date=end_date,
            converted_duration=converted_duration,
        )

    def _is_applicable_for(self, product, qty_in_product_uom, date=None, pricelists=None):
        """ Check if the rule is applicable for the given product. """
        res = super()._is_applicable_for(product, qty_in_product_uom)

        if date and self.date_start and date <= self.date_start:
            res = False
        if date and self.date_end and self.date_end <= date:
            res = False
        if pricelists and self.pricelist_id.id not in pricelists:
            res = False

        return res

    def _compute_price(self, product, quantity, uom, date, currency=None, converted_duration=None, **kwargs):
        """ Compute price based on the duration and unit. """
        price = super()._compute_price(product, quantity, uom, date, currency, **kwargs)
        if converted_duration and self.compute_price == 'fixed':
            price = price * converted_duration
        return price

    def _compute_base_price(self, product, quantity, uom, date, currency, start_date=None, end_date=None, **kwargs):
        """ Compute base price based on the duration and unit. """
        if product.rent_ok:
            converted_duration = 0
            if start_date and end_date:
                duration_vals = self._compute_duration_vals(start_date, end_date)
                converted_duration = self and duration_vals[self.recurrence_id.unit or 'day'] or 0
            rule_base = self.base or 'list_price'

            if rule_base == 'pricelist' and self.base_pricelist_id:
                price = self._get_first_suitable_rental_pricelist_id(
                    product=product,
                    date=date,
                    start_date=start_date,
                    end_date=end_date,
                    recurrence_id=self.recurrence_id,
                    pricelist=self.base_pricelist_id
                )._compute_price(product, quantity, uom, date)
                src_currency = self.base_pricelist_id.currency_id
                if src_currency != currency:
                    price = src_currency._convert(price, currency, self.env.company, date, round=False)
                if converted_duration:
                    return price * converted_duration
                return price

        return super()._compute_base_price(product, quantity, uom, date, currency, **kwargs)

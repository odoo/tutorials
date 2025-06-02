import math

from odoo import fields, models
from odoo.osv.expression import AND


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    rental_pricelist_rule_ids = fields.One2many(
        string="Rental Pricelist Rules",
        comodel_name='product.pricelist.item',
        inverse_name='product_tmpl_id',
        domain=lambda self: self._get_rental_pricelist_item_domain(),
    )

    default_recurrence_id = fields.Many2one(comodel_name='sale.temporal.recurrence', string="Default Sale Unit")

    def _get_pricelist_item_domain(self):
        return AND([
            super()._get_pricelist_item_domain(),
            [('recurrence_id', '=', False)]
        ])

    def _get_rental_pricelist_item_domain(self):
        return AND([
            self._base_pricelist_item_domain(),
            [('recurrence_id', '!=', False)]
        ])

    def _get_best_pricing_rule(self, quantity=None, date=None, uom=None, product=False, start_date=False, end_date=False, **kwargs):
        """ Return the best pricing rule for the given duration.

        :param ProductProduct product: a product recordset (containing at most one record)
        :param datetime start_date: start date of leasing period
        :param datetime end_date: end date of leasing period
        :return: least expensive pricing rule for given duration
        """
        self.ensure_one()
        best_pricing_rule = self.env['product.pricelist.item']
        if not (start_date and end_date):
            return best_pricing_rule

        pricelist = kwargs.get('pricelist', self.env['product.pricelist'])
        currency = kwargs.get('currency', self.currency_id)
        company = kwargs.get('company', self.env.company)
        duration_dict = self.env['product.pricelist.item']._compute_duration_vals(start_date, end_date)
        min_price = float("inf")  # positive infinity
        available_pricelist_ids = self.env['product.pricelist.item']._get_suitable_pricelist_ids(
            product or self, pricelist, date, start_date, end_date
        )

        if not available_pricelist_ids:
            return best_pricing_rule
        for pricelist_id in available_pricelist_ids:
            unit = pricelist_id.recurrence_id.unit
            price = pricelist_id._compute_price_rental(
                duration_dict[unit],
                unit,
                product or self,
                quantity,
                date,
                start_date,
                end_date,
                uom=uom
            )
            if pricelist_id.currency_id != currency:
                price = pricelist_id.currency_id._convert(
                    from_amount=price,
                    to_currency=currency,
                    company=company,
                    date=fields.Date.today(),
                )
            if price < min_price:
                min_price, best_pricing_rule = price, pricelist_id
        return best_pricing_rule

    def _compute_rental_default(self, duration, unit):
        """ computing default rental price when no rule is avilable for rental product """
        if duration <= 0:
            return self.list_price
        converted_duration = math.ceil(duration / self.default_recurrence_id.duration)
        return self.list_price * converted_duration

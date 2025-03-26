# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo import tools

class ProductPricing(models.Model):
    _name = 'product.pricing'
    _inherit = ['product.pricing', 'product.pricelist.item']

    recurrence_unit = fields.Char(related='recurrence_id.duration_display')
    compute_price = fields.Selection(
        selection=[
            ('percentage', "Discount"),
            ('formula', "Formula"),
            ('fixed', "Fixed Price"),
        ],
        help="Use the discount rules and activate the discount settings in order to show discount to customer.",
        index=True, default='percentage', required=True
    )

    @api.onchange('product_template_id')
    def _onchange_product_template_id(self):
        self.product_tmpl_id = self.product_template_id

    def _compute_price_rental(self, product, quantity, uom, date, currency):
        """Compute the price for a specified duration of the current pricing rental rule.
        :return float: price
        """
        product.ensure_one()
        uom.ensure_one()

        currency = currency or self.currency_id or self.env.company.currency_id
        currency.ensure_one()

        Pricing = self.env['product.pricing']

        product_uom = product.uom_id
        convert = lambda p: product_uom._compute_price(p, uom) if product_uom != uom else p

        if self.compute_price == 'fixed':
            price = convert(self.fixed_price)
        elif self.compute_price == 'percentage':
            base_price = self._compute_base_price(product, quantity, uom, date, currency)
            price = base_price - (base_price * (self.percent_price / 100)) or 0.0
        elif self.compute_price == 'formula':
            base_price = self._compute_base_price(product, quantity, uom, date, currency)
            price_limit = base_price
            price = base_price - (base_price * (self.price_discount / 100)) or 0.0

            if self.price_round:
                price = tools.float_round(price, precision_rounding=self.price_round)

            if self.price_surcharge:
                price += convert(self.price_surcharge)

            if self.price_min_margin:
                price = max(price, price_limit + convert(self.price_min_margin))

            if self.price_max_margin:
                price = min(price, price_limit + convert(self.price_max_margin))
        else:
            price = self._compute_base_price(product, quantity, uom, date, currency)

        return price

    @api.model_create_multi
    def create(self, vals_list):
        Product = self.env['product.product']
        Category = self.env['product.category']
        records = []

        for vals in vals_list:
            display_on = vals.get('display_applied_on')
            categ_id = vals.get('categ_id')
            product_tmpl_id = vals.get('product_tmpl_id')

            domain = [('rent_ok', '=', True)]

            if display_on == '2_product_category' and categ_id:
                domain.append(('categ_id', '=', categ_id))
            elif display_on == '1_product' and product_tmpl_id:
                domain.append(('product_tmpl_id', '=', product_tmpl_id))

            products = Product.search(domain)

            if not products:
                raise UserError("No rentable products found for the selected criteria.")

            for product in products:
                new_vals = vals.copy()
                new_vals.update({
                    'product_id': product.id,
                    'product_template_id': product.product_tmpl_id.id,
                    'product_tmpl_id': product.product_tmpl_id.id
                })
                records.append(new_vals)

        return super().create(records)

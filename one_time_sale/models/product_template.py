from odoo import fields, models
from odoo.tools import format_amount
from odoo.http import request


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    accept_one_time = fields.Boolean(
        string="Accept One Time",
        default=False,
        copy=False,
        help="Enable the product to sale/purchase for one-time.")

    @staticmethod
    def has_one_time_purchase(sale_order):
        """Check if the sale order contains a one-time purchase product."""
        return any(
            not line.order_id.plan_id
            and line.product_id.recurring_invoice
            and line.product_id.accept_one_time
            and line.price_unit == line.product_id.list_price
            for line in (sale_order.order_line if sale_order else [])
        )
    
    def _get_additionnal_combination_info(self, product_or_template, quantity, date, website):
        """Pass additinal information to handle the one-time purchase."""
        res = super()._get_additionnal_combination_info(product_or_template, quantity, date, website)

        pricings = res.get('pricings', [])
        # add discount per pricing plan if product is consumable product
        if product_or_template.type == 'consu' and pricings:
            one_time_price = res.get('list_price', 0) if product_or_template.accept_one_time else 0
            # base_price as one_time_price if available otherwise maximum price from all subscription plans
            base_price = one_time_price or max((pricing['price_value'] for pricing in pricings), default=0)

            if base_price > 0:
                for pricing in pricings:
                    discount = ((base_price - pricing['price_value']) / base_price * 100)
                    pricing['discount'] = f"-{round(discount, 2)}%" if discount > 0 else 0
            
            if one_time_price > 0:
                price_format = format_amount(self.env, amount=one_time_price, currency=website.currency_id)
                # add one time price if available at top of the pricings for comparison list
                pricings.insert(0, {
                    'plan_id': False,
                    'price': f"One-Time: {one_time_price}",
                    'price_value': one_time_price,
                    'table_price': price_format,
                    'table_name': "One-Time",
                    'can_be_added': True,
                    'discount': 0
                })

        sale_order = website.sale_get_order() if website else None
        res.update({
            'accept_one_time_product': product_or_template.accept_one_time,
            'product_type': product_or_template.type,
            'has_one_time_purchase': self.has_one_time_purchase(sale_order)
        })
        return res

    def _is_add_to_cart_possible(self, parent_combination=None):
        """Check whether adding the product to the cart is possible."""
        website = request and request.website
        sale_order = website and website.sale_get_order()

        if not sale_order:
            return super()._is_add_to_cart_possible(parent_combination)

        # Prevent adding a subscription product if a one-time purchase is in the cart
        if (
            self.recurring_invoice
            and self.has_one_time_purchase(sale_order)
            and (self.type != 'consu' or not self.accept_one_time)
        ):
            return False

        return super()._is_add_to_cart_possible(parent_combination)

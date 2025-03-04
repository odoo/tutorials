from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale


class RentalOrderWebsite(WebsiteSale):
    @route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        order = request.website.sale_get_order()
        deposit_product = request.env.company.deposit_product
        # print("this is deposit product", deposit_product)

        if not deposit_product or not order:
            return super().cart(access_token=access_token, revive=revive, **post)

        rental_products = order.order_line.filtered(lambda product: product.product_id.requires_deposit)
        # print("this is rental products", rental_products.product_id)
        if rental_products:
            for rental_product in rental_products:
                existing_deposit = order.order_line.filtered(
                    lambda product: product.product_id == deposit_product and product.name == f"Deposit For {rental_product.product_id.name}"
                )
                if not existing_deposit:
                    order.order_line += order.env['sale.order.line'].new({
                        'product_id': deposit_product.id,
                        'name': f"Deposit For {rental_product.product_id.name}",
                        'product_uom_qty': rental_product.product_uom_qty,
                        'price_unit': rental_product.product_id.deposit_amount,
                        'order_id': order.id
                    })

        return super().cart(access_token=access_token, revive=revive, **post)

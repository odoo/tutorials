from odoo import models, fields


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[
            ("last_purchase_price", "Last Purchase Price"),
        ],
        default="list_price",
        ondelete={"last_purchase_price": "set default"},
        help="Choose what the pricing rule should be based on:\n"
        "- Sales Price: Uses the standard sales price from the product.\n"
        "- Last Purchase Price: Uses the most recent purchase price paid for the product.",
    )


def _compute_base_price(self, product, quantity, uom=None, date=None, currency=None):
    self.ensure_one()  # this method is called per item
    if self.base == "last_purchase_price":
        # Use product's template's last purchase price
        price = product.product_tmpl_id.last_purchase_price
        if currency and product.currency_id != currency:
            price = product.currency_id._convert(
                price,
                currency,
                product.company_id or self.env.company,
                date or fields.Date.today(),
            )
        return price or 0.0  # Ensure we return a float
    else:
        # Fallback to original method
        return super(ProductPricelistItem, self)._compute_base_price(
            product, quantity, uom=uom, date=date, currency=currency
        )

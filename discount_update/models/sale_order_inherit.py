from collections import defaultdict
from odoo import _, models


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    def recalculate_discount(self):
        for order in self:
            discount_ol = order.order_line.filtered(
                lambda ol: ol.is_global_discount_line
            )
            if not discount_ol:
                return

            discount_per = discount_ol[0].discount_percentage
            discount_product = discount_ol[0].product_id
            discount_ol.unlink()
            total_price_per_tax_groups = defaultdict(float)

            for line in order.order_line:
                if not line.product_uom_qty or not line.price_unit:
                    continue

                total_price_per_tax_groups[line.tax_id] += (
                    line.price_unit * line.product_uom_qty
                )

            if not total_price_per_tax_groups:
                return

            elif len(total_price_per_tax_groups) == 1:
                taxes = next(iter(total_price_per_tax_groups.keys()))
                subtotal = total_price_per_tax_groups[taxes]
                self.env["sale.order.line"].create(
                    {
                        "order_id": order.id,
                        "product_id": discount_product.id,
                        "name": _("Discount: %(percent)s%%", percent=discount_per),
                        "product_uom_qty": 1,
                        "tax_id": [(6, 0, taxes.ids)],
                        "price_unit": -subtotal * discount_per / 100,
                    }
                )

            else:
                vals_list = [
                    (
                        {
                            "order_id": order.id,
                            "product_id": discount_product.id,
                            "name": _(
                                "Discount: %(percent)s%%"
                                "- On products with the following taxes %(taxes)s",
                                percent=discount_per,
                                taxes=", ".join(taxes.mapped("name")),
                            ),
                            "product_uom_qty": 1,
                            "tax_id": [(6, 0, taxes.ids)],
                            "price_unit": -subtotal * discount_per / 100,
                        }
                    )
                    for taxes, subtotal in total_price_per_tax_groups.items()
                ]
                self.env["sale.order.line"].create(vals_list)

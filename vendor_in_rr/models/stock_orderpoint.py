from odoo import api, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.onchange("route_id")
    def _onchange_route_as_buy_set_supplier(self):
        if (
            self.product_id
            and self.route_id
            and "buy" in self.route_id.rule_ids.mapped("action")
        ):
            if not self.supplier_id:
                best_supplier = self._get_best_supplier(self.product_id)
                if best_supplier:
                    self.supplier_id = best_supplier.id

    def _get_best_supplier(self, product):
        supplierinfos = self.env["product.supplierinfo"].search(
            [
                ("product_tmpl_id", "=", product.product_tmpl_id.id),
            ]
        )

        best_supplier = False
        best_effective_price = None

        for supplier in supplierinfos:
            # Normalize min_qty to product UoM
            normalized_min_qty = supplier.product_uom._compute_quantity(
                supplier.min_qty, product.uom_id
            )

            # Avoid division by zero
            if normalized_min_qty <= 0:
                continue

            effective_price = supplier.price / normalized_min_qty

            if (best_effective_price is None) or (
                effective_price < best_effective_price
            ):
                best_effective_price = effective_price
                best_supplier = supplier

        return best_supplier

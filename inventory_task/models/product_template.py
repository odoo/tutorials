from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    qty_input = fields.Float(
        "Quantity on Hand", compute="_compute_qty_input", inverse="_inverse_qty_input"
    )

    is_multi_location = fields.Boolean(
        compute="_compute_is_multi_location", store=False
    )

    @api.depends("company_id")
    def _compute_is_multi_location(self):
        for product in self:
            product.is_multi_location = self.env.user.has_group(
                "stock.group_stock_multi_locations"
            )

    @api.depends("qty_available")
    def _compute_qty_input(self):
        for record in self:
            record.qty_input = record.qty_available

    def _inverse_qty_input(self):
        return

    @api.onchange("qty_input")
    def _onchange_new_qty(self):
        for product in self:
            if product.qty_input >= 0:
                if not product.product_variant_id:
                    continue
                stock_quant = self.env["stock.quant"].search(
                    [
                        ("product_id", "=", product.product_variant_id.id),
                    ],
                    limit=1,
                )

                if stock_quant:
                    stock_quant.sudo().write({"quantity": product.qty_input})
                else:
                    warehouse = self.env["stock.warehouse"].search(
                        [("company_id", "=", self.env.company.id)], limit=1
                    )
                    self.env["stock.quant"].with_context(inventory_mode=True).create(
                        {
                            "product_id": product.product_variant_id.id,
                            "location_id": warehouse.lot_stock_id.id,
                            "quantity": product.qty_input,
                        }
                    )

    def action_product_replenish(self):
        return {
            "name": "Low on stock? Let's replenish.",
            "type": "ir.actions.act_window",
            "res_model": "product.replenish",
            "view_mode": "form",
            "view_id": self.env.ref("stock.view_product_replenish").id,
            "target": "new",
            "context": {
                "default_product_tmpl_id": self.id,
            },
        }

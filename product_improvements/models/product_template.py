from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    qty_available = fields.Float(inverse='_inverse_quantities')
    is_multi_location = fields.Boolean(compute="_compute_is_multi_location")

    @api.depends("company_id")
    def _compute_is_multi_location(self):
        for product in self:
            product.is_multi_location = self.env.user.has_group("stock.group_stock_multi_locations")

    @api.model_create_multi
    def create(self, vals_list):
        product = super().create(vals_list)

        for product, vals in zip(product, vals_list):
            product_variant = product.product_variant_id

            if not product_variant:
                continue

            initial_qty = vals.get('qty_available', 0)

            if initial_qty > 0:
                product._inverse_quantities(initial_qty)

        return product

    def _inverse_quantities(self, initial_qty=None):
        for template in self:
            if not template.product_variant_id:
                continue

            warehouse = self.env['stock.warehouse'].search(
                [('company_id', '=', self.env.company.id)], limit=1
            )
            if not warehouse:
                return

            stock_quant = self.env['stock.quant'].search([
                ('product_id', '=', template.product_variant_id.id),
                ('location_id', '=', warehouse.lot_stock_id.id)
            ], limit=1)
            new_qty = initial_qty if initial_qty is not None else template.qty_available
            if stock_quant:
                stock_quant.sudo().write({'inventory_quantity': new_qty})
                stock_quant._apply_inventory()
            else:
                self.env['stock.quant'].sudo().create({
                    'product_id': template.product_variant_id.id,
                    'location_id': warehouse.lot_stock_id.id,
                    'inventory_quantity': new_qty,
                })._apply_inventory()

    def action_product_replenish(self):
        return {
            "name": "Low on stock? Let's replenish.",
            "type": "ir.actions.act_window",
            "res_model": "product.replenish",
            "view_mode": "form",
            "view_id": self.env.ref("stock.view_product_replenish").id,
            "target": "new",
            "context": {"default_product_id": self.id},
        }

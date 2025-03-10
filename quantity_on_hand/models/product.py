from odoo import api, fields, models
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Add to product.product class
    qty_available = fields.Float(
        compute='_compute_quantities',
        inverse='_inverse_qty_available',  # Add inverse
        search='_search_qty_available',
        digits='Product Unit of Measure',
        compute_sudo=False
    )
    show_qty_update_button = fields.Boolean(compute='_compute_show_qty_update_button')

    @api.depends('product_tmpl_id')
    def _compute_show_qty_update_button(self):
        for product in self:
            product.show_qty_update_button = (self.env.user.has_group("stock.group_stock_multi_locations"))

    def _inverse_qty_available(self):
        """Handle direct quantity updates for single-location installations"""

        if self.env.context.get('skip_qty_available_update', False):
            return
        for product in self:
            if (product.type == "consu" and product.is_storable and product.qty_available > 0):
                warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=1)
                self.env['stock.quant'].with_context(inventory_mode=True).create({
                    'product_id': product.id,
                    'location_id': warehouse.lot_stock_id.id,
                    'inventory_quantity': product.qty_available,
                }).action_apply_inventory()

class ProductTemplate(models.Model):
    _inherit = "product.template"

    qty_available = fields.Float(
        compute='_compute_quantities',
        inverse='_inverse_qty_available',  # Add inverse
        search='_search_qty_available',
        digits='Product Unit of Measure',
        compute_sudo=False
    )

    show_qty_update_button = fields.Boolean(compute='_compute_show_qty_update_button')

    def _inverse_qty_available(self):
        if self.env.context.get('skip_qty_available_update', False):
            return
        for template in self:
            if template.qty_available and not template.product_variant_id:
                raise UserError("Save the product form before updating the Quantity On Hand.")
            else:
                template.product_variant_id.qty_available = template.qty_available

    @api.depends('product_variant_count', 'tracking')
    def _compute_show_qty_update_button(self):

        for product in self:
            product.show_qty_update_button = (
                self.env.user.has_group("stock.group_stock_multi_locations")
                or product.product_variant_count > 1
            )


            

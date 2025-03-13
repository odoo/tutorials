from odoo import models
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # -------------------------------------------------------------------------
    # METHODS
    # -------------------------------------------------------------------------

    def create_delivery_order(self, warehouse, order_lines):
        """Create a delivery order (picking) for the given warehouse and order lines."""

        delivery_picking = self.env['stock.picking'].create({
            'partner_id': self.partner_id.id,
            'picking_type_id': warehouse.out_type_id.id,
            'location_id': warehouse.lot_stock_id.id,
            'location_dest_id': self.partner_id.property_stock_customer.id,
            'origin': self.name,
        })

        for line in order_lines:
            self.env['stock.move'].create({
                'picking_id': delivery_picking.id,
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'location_id': warehouse.lot_stock_id.id,
                'location_dest_id': self.partner_id.property_stock_customer.id,
            })

        return delivery_picking

    def check_stock_availability(self, product, warehouse):
        """Check if the entire order can be fulfilled from a single warehouse."""

        stock_quant = self.env['stock.quant'].search([
            ('product_id', '=', product.id),
            ('location_id', '=', warehouse.lot_stock_id.id)
        ], limit=1)
        return stock_quant.quantity > 0 if stock_quant else False

    def can_fulfill_from_single_warehouse(self, warehouse):
        if not self.order_line:
            return False

        for line in self.order_line:
            if self.check_stock_availability(line.product_id, warehouse) == False:
                return False

        return True

    def group_lines_by_warehouse(self):
        """Group order lines by available warehouse based on stock availability."""

        warehouse_lines = {}
        for line in self.order_line:
            product = line.product_id
            primary_stock = self.check_stock_availability(
                product, product.primary_warehouse_id)
            secondary_stock = self.check_stock_availability(
                product, product.secondary_warehouse_id) if product.secondary_warehouse_id else False

            if primary_stock:
                warehouse = product.primary_warehouse_id
            elif secondary_stock:
                warehouse = product.secondary_warehouse_id
            else:
                raise ValidationError(
                    f"The product '{product.name}' has no stock in both primary and secondary warehouses.")

            if warehouse not in warehouse_lines:
                warehouse_lines[warehouse] = []
            warehouse_lines[warehouse].append(line)

        return warehouse_lines

    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------

    def action_confirm(self):
        """Confirm the sale order and create delivery orders based on stock availability."""

        primary_warehouse = self.order_line[0].product_id.primary_warehouse_id
        secondary_warehouse = self.order_line[0].product_id.secondary_warehouse_id

        if self.can_fulfill_from_single_warehouse(primary_warehouse):
            for line in self.order_line:
                line.warehouse_id = primary_warehouse # Assign all products to Primary Warehouse
            res = self.create_delivery_order(
                primary_warehouse, self.order_line)
            self.write({'picking_ids': [(4, res.id)]})
        elif secondary_warehouse and self.can_fulfill_from_single_warehouse(secondary_warehouse):
            for line in self.order_line:
                line.warehouse_id = secondary_warehouse # Assign all products to Secondary Warehouse
            res = self.create_delivery_order(
                secondary_warehouse, self.order_line)
            self.write({'picking_ids': [(4, res.id)]})
        else:
            warehouse_lines = self.group_lines_by_warehouse()
            for warehouse, lines in warehouse_lines.items():
                res = self.create_delivery_order(warehouse, lines)
                self.write({'picking_ids': [(4, res.id)]})

        self.write({'state': 'sale'})
        return True

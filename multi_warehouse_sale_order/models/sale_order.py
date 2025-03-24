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

    def check_stock_availability(self, product, warehouse, required_qty):
        """Check if a warehouse has sufficient stock for a given product."""
        stock_quant = self.env['stock.quant'].search([
            ('product_id', '=', product.id),
            ('location_id', '=', warehouse.lot_stock_id.id)
        ], limit=1)
        return stock_quant.quantity >= required_qty if stock_quant else False

    def get_fulfillment_warehouse(self):
        """Determine the best warehouse strategy to minimize delivery orders."""

        warehouse_product_count = {}
        product_warehouse_map = {}

        # Identify available warehouses for each product
        for line in self.order_line:
            product = line.product_id
            primary_warehouse = product.primary_warehouse_id
            secondary_warehouse = product.secondary_warehouse_id

            available_warehouses = []
            if self.check_stock_availability(product, primary_warehouse, line.product_uom_qty):
                available_warehouses.append(primary_warehouse)
            if secondary_warehouse and self.check_stock_availability(product, secondary_warehouse, line.product_uom_qty):
                available_warehouses.append(secondary_warehouse)

            if not available_warehouses:
                raise ValidationError(f"Product '{product.name}' is out of stock in warehouses.")

            # Count how many products each warehouse can fulfill
            for warehouse in available_warehouses:
                warehouse_product_count.setdefault(warehouse, 0)
                warehouse_product_count[warehouse] += 1

            product_warehouse_map[product] = available_warehouses

        sorted_warehouses = sorted(warehouse_product_count, key=warehouse_product_count.get, reverse=True)

        final_warehouse_assignment = {}

        for product, available_warehouses in product_warehouse_map.items():
            assigned_warehouse = None
            for wh in sorted_warehouses:
                if wh in available_warehouses:
                    assigned_warehouse = wh
                    break

            if assigned_warehouse:
                for line in self.order_line:
                    if line.product_id == product:
                        line.write({'warehouse_id': assigned_warehouse.id})  # Update SOL warehouse
                        if assigned_warehouse not in final_warehouse_assignment:
                            final_warehouse_assignment[assigned_warehouse] = []
                        final_warehouse_assignment[assigned_warehouse].append(line)
                        break

        return final_warehouse_assignment

    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------

    def action_confirm(self):
        """Confirm the sale order and create optimized delivery orders."""
        warehouse_lines = self.get_fulfillment_warehouse()

        for warehouse, lines in warehouse_lines.items():
            res = self.create_delivery_order(warehouse, lines)
            self.write({'picking_ids': [(4, res.id)]})

        self.write({'state': 'sale'})
        return True

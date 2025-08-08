from odoo.addons.stock.tests.common import TestStockCommon
from odoo.tests import Form
from odoo.tests import tagged

class TestMassReturnPicking(TestStockCommon):

    def test_mass_return_picking(self):
        StockReturnObj = self.env["stock.return.picking"]
        SaleOrderObj = self.env["sale.order"]
        SaleOrderLineObj = self.env["sale.order.line"]
        ReturnPickingLineObj = self.env["stock.return.picking.line"]

        # Use default test customer
        customer = self.env.ref("base.res_partner_2")

        # Create Sale Order 1
        sale_order_1 = SaleOrderObj.create({
            "partner_id": customer.id,
            "order_line": [(0, 0, {
                "product_id": self.UnitA.id,
                "product_uom_qty": 3,
                "product_uom": self.uom_unit.id,
                "price_unit": 100.0,
            })]
        })
        sale_order_1.action_confirm() 

        # Create Sale Order 2
        sale_order_2 = SaleOrderObj.create({
            "partner_id": customer.id,
            "order_line": [(0, 0, {
                "product_id": self.kgB.id,
                "product_uom_qty": 5,
                "product_uom": self.uom_kg.id,
                "price_unit": 200.0,
            })]
        })
        sale_order_2.action_confirm() 

        # Get the pickings generated automatically from the sale orders
        picking_out_1 = sale_order_1.picking_ids.filtered(lambda p: p.state not in ["done", "cancel"])
        picking_out_2 = sale_order_2.picking_ids.filtered(lambda p: p.state not in ["done", "cancel"])

        self.assertTrue(picking_out_1, "Sale Order 1 should generate a picking")
        self.assertTrue(picking_out_2, "Sale Order 2 should generate a picking")

        # Confirm and validate pickings
        for picking in [picking_out_1, picking_out_2]:
            picking.action_confirm()
            picking.action_assign()
            for move in picking.move_ids:
                move.quantity = move.product_uom_qty  # Set quantity as done
            picking.move_ids.picked = True
            picking.button_validate()

        # Create mass return with selected pickings
        return_wizard = StockReturnObj.with_context(
            active_ids=[picking_out_1.id, picking_out_2.id],
            active_model="stock.picking"
        ).create({})

        # Ensure allowed products are correctly set
        allowed_product_ids = return_wizard.allowed_product_ids.ids
        self.assertIn(self.UnitA.id, allowed_product_ids, "Allowed products should include UnitA")
        self.assertIn(self.kgB.id, allowed_product_ids, "Allowed products should include kgB")

        # Create a return line where product_id and sale_order_id exist
        return_line = ReturnPickingLineObj.create({
            "wizard_id": return_wizard.id,
            "product_id": self.UnitA.id,
        })
        return_line._onchange_product_id()

        # Check if allowed_sale_order_ids has values
        self.assertTrue(return_line.allowed_sale_order_ids, "allowed_sale_order_ids should have at least one sale order")
        self.assertIsNotNone(return_line.sale_order_id, "sale_order_id should be automatically set if only one option exists")

        return_line._onchange_picking_id()
        # Validate final return
        return_wizard.action_create_returns()

from odoo.tests import TransactionCase


class TestSubProdcut(TransactionCase):
    def setUp(self):
        childproduct1 = self.env["product.template"].create({"name": "Child1"})
        childproduct2 = self.env["product.template"].create({"name": "Child2"})
        self.product1 = self.env["product.product"].search(
            [("product_tmpl_id", "=", childproduct1.id)]
        )
        self.product2 = self.env["product.product"].search(
            [("product_tmpl_id", "=", childproduct2.id)]
        )

        parentproduct = self.env["product.template"].create(
            {
                "name": "parent",
                "is_kit": True,
                "sub_product_ids": [self.product1.id, self.product2.id],
            }
        )
        self.parent_product = self.env["product.product"].search(
            [("product_tmpl_id", "=", parentproduct.id)]
        )

        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.env.ref("base.partner_demo").id,
            }
        )
        self.parentline = self.env["sale.order.line"].create(
            {
                "product_id": self.parent_product.id,
                "order_id": sale_order.id,
                "product_uom_qty": 1,
                "name": self.parent_product.name,
            }
        )
        self.childline1 = self.env["sale.order.line"].create(
            {
                "product_template_id": self.product1.id,
                "order_id": sale_order.id,
                "product_uom_qty": 3,
                "parent_line_id": self.parentline.id,
                "name": self.product1.name,
            }
        )
        self.childline2 = self.env["sale.order.line"].create(
            {
                "product_template_id": self.product2.id,
                "order_id": sale_order.id,
                "product_uom_qty": 2,
                "parent_line_id": self.parentline.id,
                "name": self.product2.name,
            }
        )

    def test_parent_quantity_update_child(self):
        old_parent_qty = self.parentline.product_uom_qty
        old_child_qty1 = self.childline1.product_uom_qty
        old_child_qty2 = self.childline2.product_uom_qty

        new_parent_qty = 4
        self.parentline.write({"product_uom_qty": new_parent_qty})

        new_child_qty1 = (old_child_qty1 / old_parent_qty) * new_parent_qty
        new_child_qty2 = (old_child_qty2 / old_parent_qty) * new_parent_qty

        self.assertEqual(
            self.childline1.product_uom_qty,
            new_child_qty1,
            f"expected {new_child_qty1}, but got {self.childline1.product_uom_qty}",
        )
        self.assertEqual(
            self.childline2.product_uom_qty,
            new_child_qty2,
            f"expected {new_child_qty2}, but got {self.childline2.product_uom_qty}",
        )

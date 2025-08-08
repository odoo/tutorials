from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo import Command

@tagged("post_install", "-at_install")
class TestRequiredAttributes(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestRequiredAttributes, cls).setUpClass()

        cls.test_required_attribute = cls.env["product.attribute"].create({
            "name": "Required Attribute"
        })
        cls.test_required_values = cls.env["product.attribute.value"].create([
            {
                "name": "Required Attribute 1",
                "attribute_id": cls.test_required_attribute.id
            },
            {
                "name": "Required Attribute 2",
                "attribute_id": cls.test_required_attribute.id
            },
            {
                "name": "Required Attribute 3",
                "attribute_id": cls.test_required_attribute.id
            }
        ])

        cls.test_attribute = cls.env["product.attribute"].create({
            "name": "Normal Attribute"
        })
        cls.test_attribute_values = cls.env["product.attribute.value"].create([
            {
                "name": "Attribute 1",
                "attribute_id": cls.test_attribute.id
            }, 
            {
                "name": "Attribute 2",
                "attribute_id": cls.test_attribute.id
            },
            {
                "name": "Attribute 3",
                "attribute_id": cls.test_attribute.id
            }
        ])

        cls.category = cls.env['product.category'].create([{
            'name': 'Test Category',
            'show_on_global_info': True,
            'required_attribute_ids': [Command.set([cls.test_required_attribute.id])]
        }])

        cls.product = cls.env["product.product"].create({
            "name": "Test Product",
            "categ_id": cls.category.id,
            "attribute_line_ids": [Command.create({
                "attribute_id": cls.test_required_attribute.id,
                "value_ids": [Command.set(cls.test_required_values.ids)]
            }), Command.create({
                "attribute_id": cls.test_attribute.id,
                "value_ids": [Command.set(cls.test_attribute_values.ids)]
            })]
        })


        cls.sale_order = cls.env["sale.order"].create({"partner_id": cls.env.ref("base.res_partner_1").id})
        cls.sale_order_line = cls.env["sale.order.line"].create({
            "order_id": cls.sale_order.id,
            "product_id": cls.product.id
        })

    def test_category_fields(self):
        self.assertTrue(self.category.show_on_global_info, "Category should have 'show_on_global_info' set to True")
        self.assertEqual(len(self.category.required_attribute_ids), 1, "Category should have one required attributes (test_required_attribute)")

    def test_product_attributes(self):
        product_attributes = self.product.attribute_line_ids.mapped("attribute_id.name")
        self.assertIn("Required Attribute", product_attributes, "Product should have 'Required Attribute' in attribute")
        self.assertIn("Normal Attribute", product_attributes, "Product should have 'Normal Attribute' in attribute")

    def test_sale_order_line_global_info(self):
        if self.sale_order_line.product_id.categ_id.show_on_global_info:
            displayed_attributes = self.sale_order_line.product_id.categ_id.required_attribute_ids.mapped("name")
            self.assertIn("Required Attribute", displayed_attributes, "Global info should show 'Required Attribute'")
            self.assertNotIn("Normal Attribute", displayed_attributes, "Global info should NOT show 'Normal Attribute'")

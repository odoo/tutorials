from odoo.exceptions import UserError

from odoo.fields import Command
from odoo.tests.common import tagged, TransactionCase


@tagged('post_install', '-at_install')
class TestDefaultAttribute(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner1 = cls.env['res.partner'].create({'name': 'Partner1'})

        cls.Attr1 = cls.env['product.attribute'].create({
            'name': 'Attr1',
        })

        cls.Attr2 = cls.env['product.attribute'].create({
            'name': 'Attr2',
            'value_ids': [
                Command.create({
                    'name': 'Attr2Value1',
                }),
                Command.create({
                    'name': 'Attr2Value2',
                }),
            ],
        })

        cls.Attr3 = cls.env['product.attribute'].create({
            'name': 'Attr3',
            'value_ids': [
                Command.create({
                    'name': 'Attr3Value1',
                }),
                Command.create({
                    'name': 'Attr3Value2',
                }),
            ],
        })

        cls.Attr4 = cls.env['product.attribute'].create({
            'name': 'Attr4',
            'value_ids': [
                Command.create({
                    'name': 'Attr4Value1',
                }),
            ],
        })

        cls.parent_product_category = cls.env['product.category'].create({
            'name': 'All',
        })

        cls.product_category1 = cls.env['product.category'].create({
            'name': 'Categ1',
            'parent_id': cls.parent_product_category.id,
            'show_on_global_info': True,
        })

        cls.product_category2 = cls.env['product.category'].create({
            'name': 'Categ2',
            'parent_id': cls.parent_product_category.id,
            'default_attribute_ids': [
                cls.Attr1.id,
            ],
        })

        cls.product_category3 = cls.env['product.category'].create({
            'name': 'Categ3',
            'parent_id': cls.parent_product_category.id,
            'show_on_global_info': True,
            'default_attribute_ids': [
                cls.Attr2.id,
            ],
        })

        cls.product_category4 = cls.env['product.category'].create({
            'name': 'Categ4',
            'parent_id': cls.parent_product_category.id,
            'show_on_global_info': True,
            'default_attribute_ids': [
                cls.Attr3.id,
                cls.Attr4.id,
            ],
        })

        cls.product_template1 = cls.env['product.template'].create({
            'name': 'Test Product1',
            'categ_id': cls.product_category1.id,
            'list_price': 100.0,
            'standard_price': 80.0,
            'type': 'consu',
        })

        cls.sale_order1 = cls.env['sale.order'].create({
            'partner_id': cls.partner1.id,
        })

    def test_global_info_line_intially(self):
        global_info_line_categories = self.sale_order1.global_info_line_ids.mapped('product_category_id')
        expected_categories = self.product_category3 | self.product_category4
        self.assertEqual(global_info_line_categories, expected_categories, "Global info line does not contain the correct categories.")

        global_info_line_attributes = self.sale_order1.global_info_line_ids.mapped('attribute_id')
        expected_attributes = self.Attr2 | self.Attr3 | self.Attr4
        self.assertEqual(global_info_line_attributes, expected_attributes, "Global info line does not contain the correct attributes.")

    def test_global_info_line_after_change_in_product_category(self):
        self.product_category2.show_on_global_info = True
        global_info_line_categories = self.sale_order1.global_info_line_ids.mapped('product_category_id')
        expected_categories = self.product_category2 | self.product_category3 | self.product_category4
        self.assertEqual(global_info_line_categories, expected_categories, "Global info line does not contain the correct "
            "categories after change in the product category.")

        global_info_line_attributes = self.sale_order1.global_info_line_ids.mapped('attribute_id')
        expected_attributes = self.Attr1 | self.Attr2 | self.Attr3 | self.Attr4
        self.assertEqual(global_info_line_attributes, expected_attributes, "Global info line does not contain the correct "
            "attributes after change in the product category.")

        self.product_category4.default_attribute_ids = self.Attr3
        new_global_info_line_attributes = self.sale_order1.global_info_line_ids.mapped('attribute_id')
        new_expected_attributes = self.Attr1 | self.Attr2 | self.Attr3
        self.assertEqual(new_global_info_line_attributes, new_expected_attributes, "Global info line does not contain the correct "
            "attributes after change in the product category default attributes.")

    def test_default_attributes_on_product_template(self):
        product_attributes = self.product_template1.attribute_line_ids.mapped('attribute_id.id')
        self.assertEqual(product_attributes, [], "When a product category that has no default attributes is selected in the "
            "product template, the product attributes on product template should be empty.")

        self.product_template1.categ_id = self.product_category3.id
        new_product_attributes = self.product_template1.attribute_line_ids.mapped('attribute_id')
        expected_attributes = self.Attr2
        self.assertEqual(new_product_attributes, expected_attributes, "When a product category that has default attributes "
            "is selected in the product template, the product attributes on product template should be equal to that default attributes.")

    def test_attributes_on_product_template_after_change_in_category(self):
        self.product_template1.categ_id = self.product_category3.id
        self.product_category3.default_attribute_ids = (self.Attr3.id, self.Attr4.id)
        new_product_attributes = self.product_template1.attribute_line_ids.mapped('attribute_id')
        expected_attributes = self.Attr3 | self.Attr4
        self.assertEqual(new_product_attributes, expected_attributes, "Attributes on the product form does not match with "
            "default attributes of category after change in it")

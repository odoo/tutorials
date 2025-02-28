from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo import Command


@tagged("post_install", "-at_install")
class TestCartRelatedProducts(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product_a_template = cls.env['product.template'].create({
            'name': 'product A'
        })
        cls.product_b_template = cls.env['product.template'].create({
            'name': 'product B'
        })
        cls.product_c_template = cls.env['product.template'].create({
            'name': 'product C'
        })
        cls.product_d_template = cls.env['product.template'].create({
            'name': 'product D'
        })
        
        cls.product_a = cls.product_a_template.product_variant_id
        cls.product_b = cls.product_b_template.product_variant_id
        cls.product_c = cls.product_c_template.product_variant_id
        cls.product_d = cls.product_d_template.product_variant_id

        cls.product_a_template.write({
            'related_product_ids': [Command.set([cls.product_b_template.id, cls.product_c_template.id])]
        })
        cls.product_b_template.write({
            'related_product_ids': [Command.set([cls.product_d_template.id])]
        })
        cls.product_d_template.write({
            'related_product_ids': [Command.set([cls.product_a_template.id])]
        })

        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.env.ref('base.res_partner_1').id
        })

    def test_add_related_products_of_actual_product(self):
        self.sale_order._cart_update(product_id=self.producta.id, add_qty=1)
        product_ids = self.sale_order.order_line.mapped('product_id')

        self.assertIn(self.producta, product_ids, "Product a should be in the cart")
        self.assertIn(self.productb, product_ids, "Product b should be automatically added")
        self.assertIn(self.productc, product_ids, "Product c should be automatically added")
        self.assertNotIn(self.productd, product_ids, "Product d should not be added")

    def test_remove_actual_product_and_its_related_product(self):
        self.sale_order._cart_update(product_id=self.producta.id, add_qty=1)
        self.sale_order._cart_update(product_id=self.producta.id, add_qty=-1)
        
        product_ids = self.sale_order.order_line.mapped('product_id')

        self.assertNotIn(self.producta, product_ids, "Product a should be removed from the cart")
        self.assertNotIn(self.productb, product_ids, "Product b should be removed from the cart")
        self.assertNotIn(self.productc, product_ids, "Product c should be removed from the cart")

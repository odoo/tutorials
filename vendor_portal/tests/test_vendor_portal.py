# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import HttpCase, tagged


@tagged("-at_install", "post_install")
class TestVendorPortal(HttpCase):

    def setUp(self):
        super().setUp()

        self.country = self.env["res.country"].create({"name": "Testportalland", "code": "TP"})
        self.vendor = self.env["res.partner"].create({
            "name": "Test Vendor",
            "country_id": self.country.id,
            "supplier_rank": 1,
        })
        self.category = self.env["product.public.category"].create({"name": "Test Category"})
        self.product_template = self.env["product.template"].create({
            "name": "Test Product",
            "type": "consu",
            "public_categ_ids": [(6, 0, [self.category.id])],
            "seller_ids": [(0, 0, {
                "partner_id": self.vendor.id,
                "min_qty": 1.0,
                "price": 100.0,
            })],
        })
        self.product = self.product_template.product_variant_id

    def test_create_purchase_order(self):
        """Test Purchase Order creation through form."""
        self.authenticate("admin", "admin")
        response = self.url_open(
            "/create-purchase-order",
            data = {
                "product_id": self.product_template.id,
                "vendor_id": self.vendor.id,
            },
        )
        self.assertEqual(response.status_code, 200)
        po = self.env["purchase.order"].search([("partner_id", "=", self.vendor.id)], limit=1)
        self.assertTrue(po)
        self.assertEqual(po.state, "draft")
        self.assertEqual(len(po.order_line), 1)
        self.assertEqual(po.order_line.product_id, self.product)
        self.assertEqual(po.order_line.product_qty, 1.0)

    def test_merge_purchase_order_same_vendor(self):
        """Test merging into an existing draft PO for same vendor"""
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.vendor.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_qty': 1.0,
            })]
        })
        self.authenticate("admin", "admin")
        self.url_open(
            "/create-purchase-order",
            data = {
                "product_id": self.product_template.id,
                "vendor_id": self.vendor.id,
            },
        )
        self.assertEqual(len(purchase_order.order_line), 1)
        self.assertEqual(purchase_order.order_line.product_qty, 2.0)
        self.assertEqual(purchase_order.order_line.price_subtotal, 200)

    def test_add_different_product_to_existing_po(self):
        """Test adding new product line when product differs"""
        second_product_template = self.env['product.template'].create({
            "name": "Test Product",
            "type": "consu",
            "public_categ_ids": [(6, 0, [self.category.id])],
            "seller_ids": [(0, 0, {
                "partner_id": self.vendor.id,
                "min_qty": 1.0,
                "price": 500.0,
            })],
        })
        second_product = second_product_template.product_variant_id
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.vendor.id,
            'order_line': [(0, 0, {
                'product_id': second_product.id,
                'product_qty': 1.0,
            })]
        })
        self.authenticate("admin", "admin")
        self.url_open(
            "/create-purchase-order",
            data = {
                "product_id": self.product_template.id,
                "vendor_id": self.vendor.id,
            },
        )
        self.assertEqual(len(purchase_order.order_line), 2)
        product_ids = purchase_order.order_line.mapped('product_id.id')
        self.assertIn(self.product.id, product_ids)
        self.assertIn(second_product.id, product_ids)

    def test_invalid_product_vendor(self):
        """Test redirect without creation if product/vendor is invalid"""
        self.authenticate("admin", "admin")
        response = self.url_open(
            "/create-purchase-order",
            data = {
                "product_id": 9999,
                "vendor_id": 9999,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('error=1', response.url)

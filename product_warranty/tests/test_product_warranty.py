from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo import Command

@tagged("post_install", "-at_install")
class TestProductWarranty(TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        cls.partner = cls.env['res.partner'].create({
            'name': "Test Partner",
        })

        cls.product_with_warranty = cls.env['product.product'].create({
            'name': "Product with Warranty",
            'is_warranty': True,
            'type': 'consu',
            'list_price': 100.0,
        })

        cls.product_without_warranty = cls.env['product.product'].create({
            'name': "Product without Warranty",
            'is_warranty': False,
            'type': 'consu',
            'list_price': 50.0,
        })

        cls.extended_warranty_product = cls.env['product.product'].create({
            'name': "Extended Warranty Product",
            'type': 'service',
        })

        cls.warranty_config_1year = cls.env['product.warranty.config'].create({
            'name': '1 Year',
            'product_template_id': cls.extended_warranty_product.product_tmpl_id.id,   
            'percentage': 10.0,
            'year': 1,
        })

        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'order_line': [
                Command.create({
                    'product_id': product.id,
                    'product_uom_qty': 1,
                })
                for product in [cls.product_with_warranty, cls.product_without_warranty]
            ]
        })

    def test_warranty_products_listed_in_wizard(self):
        """Test that only products with `is_warranty=True` are listed in the warranty wizard."""
        
        wizard = self.env['product.warranty'].create({'sale_order_id': self.sale_order.id})

        products_in_wizard = wizard.warranty_line_ids.mapped('sale_order_line_id.product_id')

        self.assertIn(
            self.product_with_warranty,
            products_in_wizard,
            "Product with warranty should be listed in wizard",
        )

    def test_add_warranty_to_sale_order(self):
        """Test that a warranty is correctly added to a Sale Order product."""
        sale_order_line_p1 = self.sale_order.order_line.filtered(lambda l: l.product_id == self.product_with_warranty)
        warranty_wizard = self.env['product.warranty'].create({
            'sale_order_id': self.sale_order.id,
            'warranty_line_ids': [
                Command.create({
                    'sale_order_line_id': sale_order_line_p1.id,
                    'product_warranty_config_id': self.warranty_config_1year.id,
                })
            ]
        })
        warranty_line = warranty_wizard.warranty_line_ids[0]

        self.assertEqual(
            warranty_line.sale_order_line_id,
            sale_order_line_p1,
            "Warranty line should be linked to the correct Sale Order line",
        )
        self.assertEqual(
            warranty_line.product_warranty_config_id,
            self.warranty_config_1year,
            "Warranty should be correctly assigned",
        )

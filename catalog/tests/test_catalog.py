# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestCatalogModule(TransactionCase):
    
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company

        cls.product_tmpl = cls.env['product.template'].create({
            'name': "Test Product Template",
            'list_price': 100.0,
            'standard_price': 50.0,
        })
        

        cls.partner = cls.env['res.partner'].create({
            'name': "Test Partner",
        })
        
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
        })

        cls.sale_order_lines = cls.env['sale.order.line'].create([
            {   'name': 'sale_order_line',
                'order_id': cls.sale_order.id,
                'product_template_id': cls.product_tmpl.id,
                'price_unit': 50.0,
                'state': 'sale',
            },
            {   
                'name': 'sale_order_line',
                'order_id': cls.sale_order.id,
                'product_template_id': cls.product_tmpl.id,
                'price_unit': 55.0,
                'state': 'sale',
            }
        ])

        cls.category = cls.env['product.category'].create({
            'name': "Furniture",
        })

        cls.catalog = cls.env['catalog.catalog'].create({
            'name': "Furniture Catalog",
            'company_id': cls.company.id,
            'catalog_line_ids': [
                Command.create({
                    'product_category_id': cls.category.id,
                    'color1': "Red",
                    'color2': "Blue",
                }),
            ],
            'catalog_fields_line_ids': [
                Command.create({
                    'fields': "name"
                }),
            ],
        })
    
    def test_catalog_creation(self):
        self.assertTrue(self.catalog, "Catalog was not created.")
        self.assertEqual(self.catalog.name, "Furniture Catalog", "Catalog name mismatch.")
        self.assertEqual(self.catalog.company_id, self.company, "Company mismatch!")    

    def test_catalog_line_creation(self):
        self.assertEqual(len(self.catalog.catalog_line_ids), 1, "Catalog line was not created.")
        catalog_line = self.catalog.catalog_line_ids[0]
        self.assertEqual(catalog_line.product_category_id, self.category, "Category mismatch in catalog lines!")
        self.assertEqual(catalog_line.color1, "Red", "Color1 mismatch!")
        self.assertEqual(catalog_line.color2, "Blue", "Color2 mismatch!")
        
    def test_catalog_field_creation(self):
        self.assertEqual(len(self.catalog.catalog_fields_line_ids), 1, "Catalog field was not created.")
        self.assertEqual(self.catalog.catalog_fields_line_ids[0].fields, "name", "Catalog field name mismatch.")   
        
    def test_product_gross_profit_margin(self):
        self.assertEqual(self.product_tmpl.gross_profit_margin, 50.0, "Gross profit margin should be 50%")

        self.product_tmpl.gross_profit_margin = 20.0
        self.assertAlmostEqual(self.product_tmpl.list_price, 62.5, places=2, msg="List price should adjust correctly based on margin")    

    def test_invalid_margin(self):
        with self.assertRaises(UserError, msg="Should not allow -100% margin"):
            self.product_tmpl.gross_profit_margin = -100
        
        with self.assertRaises(UserError, msg="Should not allow 100% margin"):
            self.product_tmpl.gross_profit_margin = 100  
            
    def test_price_list_wizard(self):
        self.env.context = {'active_id': self.sale_order_lines[0].id}

        price_wizard = self.env['price.list.wizard'].create({})
        self.assertEqual(len(price_wizard.list_ids), 0, "Price list wizard should fetch past 0 prices.")

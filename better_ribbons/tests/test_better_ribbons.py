from dateutil.relativedelta import relativedelta
from odoo import Command, fields
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestBetterRibbons(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.website = cls.env['website'].create({'name': 'Test Website'})

        cls.normal_pricelist = cls.env['product.pricelist'].create({
            'name': 'Normal Test',
            'website_id': cls.website.id,
            'selectable': True,
            'item_ids': [Command.create({'compute_price': 'percentage'})],
        })

        cls.sale_pricelist = cls.env['product.pricelist'].create({
            'name': 'Sale Test',
            'website_id': cls.website.id,
            'selectable': True,
            'item_ids': [
                Command.create({'compute_price': 'percentage', 'percent_price': 20})
            ],
        })

        cls.product = cls.env['product.template'].create({
            'name': 'Test Product',
            'is_published': True,
            'is_storable': True,
            'list_price': 100.0,
            'standard_price': 30.0,
            'allow_out_of_stock_order': True,
            'has_manual_ribbon': False,
            'website_ribbon_id': False,
            'publish_date': fields.Date.today() - relativedelta(days=5),
        })

        cls.website.write({'pricelist_id': cls.normal_pricelist.id})
        cls.prices = cls.product._get_sales_prices(cls.website)

    def _create_ribbon(self, name, assign='manually', style='ribbon', **kwargs):
        return self.env['product.ribbon'].create({
            'name': name,
            'assign': assign,
            'style': style,
            **kwargs,
        })

    def test_1_new_ribbon(self):
        ribbon4 = self._create_ribbon('New4', 'new', new_until=4)
        self.product._set_ribbon(self.prices)

        self.assertNotEqual(
            self.product.website_ribbon_id.id,
            ribbon4.id,
            'New ribbon (4day) should not be assigned to the product when publish date is more than 4 days away.',
        )

        ribbon6 = self._create_ribbon('New6', 'new', new_until=6)
        self.product._set_ribbon(self.prices)

        self.assertEqual(
            self.product.website_ribbon_id.id,
            ribbon6.id,
            'New ribbon (6day) should be assigned to the product when publish date is under 6 days away.',
        )

    def test_2_sale_ribbon(self):
        self._create_ribbon('New', 'new')
        self.product.write({'compare_list_price': 150.0})
        self.prices = self.product._get_sales_prices(self.website)
        ribbon = self._create_ribbon('Sale', 'sale')
        self.product._set_ribbon(self.prices)

        self.assertEqual(
            self.product.website_ribbon_id.id,
            ribbon.id,
            'Sale ribbon should be assigned to the product when compare price is set.',
        )

        self.product.with_context(auto_assign_ribbon=True).write({
            'website_ribbon_id': False,
            'compare_list_price': False,
        })
        self.website.write({'pricelist_id': self.sale_pricelist.id})
        self.prices = self.product._get_sales_prices(self.website)
        self.product._set_ribbon(self.prices)

        self.assertEqual(
            self.product.website_ribbon_id.id,
            ribbon.id,
            'Sale ribbon should be assigned to the product when discount is applied.',
        )

    def test_3_out_of_stock_ribbon(self):
        self.product.write({'qty_available': 0, 'allow_out_of_stock_order': False})
        self._create_ribbon('Sale', 'sale')
        self._create_ribbon('New', 'new')

        oos_ribbon = self._create_ribbon('Out of Stock', 'out_of_stock')
        self.product._set_ribbon(self.prices)

        self.assertEqual(
            self.product.website_ribbon_id.id,
            oos_ribbon.id,
            'Out of Stock ribbon should take priority over Sale ribbon.',
        )

    def test_4_manual_ribbon(self):
        manual = self._create_ribbon('Manual', 'manually')
        self.product.write({
            'website_ribbon_id': manual.id,
            'publish_date': fields.Date.today(),
        })
        self._create_ribbon('New', 'new')
        self.product._set_ribbon(self.prices)

        self.assertEqual(
            self.product.website_ribbon_id.id,
            manual.id,
            'Automatic ribbons should not override manually assigned ribbons.',
        )

    def test_5_allow_out_of_stock_flag(self):
        ribbon = self._create_ribbon('Out of Stock', 'out_of_stock')

        self.product.write({'qty_available': 0, 'allow_out_of_stock_order': True})
        self.product._set_ribbon(self.prices)
        self.assertNotEqual(
            self.product.website_ribbon_id.id,
            ribbon.id,
            'When allow_out_of_stock_order is True,'
            'the Out of Stock ribbon should not be assigned.',
        )
